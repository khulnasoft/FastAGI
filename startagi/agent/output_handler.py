import json
from fastagi.agent.common_types import TaskExecutorResponse, ToolExecutorResponse
from fastagi.agent.output_parser import AgentSchemaOutputParser
from fastagi.agent.task_queue import TaskQueue
from fastagi.agent.tool_executor import ToolExecutor
from fastagi.helper.json_cleaner import JsonCleaner
from fastagi.lib.logger import logger
from langchain.text_splitter import TokenTextSplitter
from fastagi.models.agent import Agent
from fastagi.models.agent_execution import AgentExecution
from fastagi.models.agent_execution_feed import AgentExecutionFeed
from fastagi.vector_store.base import VectorStore
import numpy as np

from fastagi.models.agent_execution_permission import AgentExecutionPermission


class ToolOutputHandler:
    """Handles the tool output response from the thinking step"""
    def __init__(self,
                 agent_execution_id: int,
                 agent_config: dict,
                 tools: list,
                 memory:VectorStore=None,
                 output_parser=AgentSchemaOutputParser()):
        self.agent_execution_id = agent_execution_id
        self.task_queue = TaskQueue(str(agent_execution_id))
        self.agent_config = agent_config
        self.tools = tools
        self.output_parser = output_parser
        self.memory=memory

    def handle(self, session, assistant_reply):
        """Handles the tool output response from the thinking step.
        Step takes care of permission control as well at tool level.

        Args:
            session (Session): The database session.
            assistant_reply (str): The assistant reply.
        """
        response = self._check_permission_in_restricted_mode(session, assistant_reply)
        if response.is_permission_required:
            return response

        tool_response = self.handle_tool_response(session, assistant_reply)
        # print(tool_response)

        agent_execution = AgentExecution.find_by_id(session, self.agent_execution_id)
        agent_execution_feed = AgentExecutionFeed(agent_execution_id=self.agent_execution_id,
                                                  agent_id=self.agent_config["agent_id"],
                                                  feed=assistant_reply,
                                                  role="assistant",
                                                  feed_group_id=agent_execution.current_feed_group_id)
        session.add(agent_execution_feed)
        tool_response_feed = AgentExecutionFeed(agent_execution_id=self.agent_execution_id,
                                                agent_id=self.agent_config["agent_id"],
                                                feed=tool_response.result,
                                                role="system",
                                                feed_group_id=agent_execution.current_feed_group_id)
        session.add(tool_response_feed)
        session.commit()
        if not tool_response.retry:
            tool_response = self._check_for_completion(tool_response)

        self.add_text_to_memory(assistant_reply, tool_response.result)
        return tool_response

    def add_text_to_memory(self, assistant_reply,tool_response_result):
        """
        Adds the text generated by the assistant and tool response to the memory.

        Args:
            assistant_reply (str): The assistant reply.
            tool_response_result (str): The tool response.

        Returns:
            None
        """
        if self.memory is not None:
            try:
                data = json.loads(assistant_reply)
                task_description = data['thoughts']['text']
                final_tool_response = tool_response_result
                prompt = task_description + final_tool_response
                text_splitter = TokenTextSplitter(chunk_size=1024, chunk_overlap=10)
                chunk_response = text_splitter.split_text(prompt)
                metadata = {"agent_execution_id": self.agent_execution_id}
                metadatas = []
                for _ in chunk_response:
                    metadatas.append(metadata)

                self.memory.add_texts(chunk_response, metadatas)
            except Exception as exception:
                logger.error(f"Exception: {exception}")
        
     

    def handle_tool_response(self, session, assistant_reply):
        """Only handle processing of tool response"""
        action = self.output_parser.parse(assistant_reply)
        agent = session.query(Agent).filter(Agent.id == self.agent_config["agent_id"]).first()
        organisation = agent.get_agent_organisation(session)
        tool_executor = ToolExecutor(organisation_id=organisation.id, agent_id=agent.id, tools=self.tools, agent_execution_id=self.agent_execution_id)
        return tool_executor.execute(session, action.name, action.args)

    def _check_permission_in_restricted_mode(self, session, assistant_reply: str):
        action = self.output_parser.parse(assistant_reply)
        tools = {t.name: t for t in self.tools}

        excluded_tools = [ToolExecutor.FINISH, '', None]

        if self.agent_config["permission_type"].upper() == "RESTRICTED" and action.name not in excluded_tools and \
                tools.get(action.name) and tools[action.name].permission_required:
            new_agent_execution_permission = AgentExecutionPermission(
                agent_execution_id=self.agent_execution_id,
                status="PENDING",
                agent_id=self.agent_config["agent_id"],
                tool_name=action.name,
                assistant_reply=assistant_reply)

            session.add(new_agent_execution_permission)
            session.commit()
            return ToolExecutorResponse(is_permission_required=True, status="WAITING_FOR_PERMISSION",
                                        permission_id=new_agent_execution_permission.id)
        return ToolExecutorResponse(status="PENDING", is_permission_required=False)

    def _check_for_completion(self, tool_response):
        self.task_queue.complete_task(tool_response.result)
        current_tasks = self.task_queue.get_tasks()
        if self.task_queue.get_completed_tasks() and len(current_tasks) == 0:
            tool_response.status = "COMPLETE"
        if current_tasks and tool_response.status == "COMPLETE":
            tool_response.status = "PENDING"
        return tool_response


class TaskOutputHandler:
    """Handles the task output from the LLM. Output is mostly in the array of tasks and
    handler adds every task to the task queue.
    """

    def __init__(self, agent_execution_id: int, agent_config: dict):
        self.agent_execution_id = agent_execution_id
        self.task_queue = TaskQueue(str(agent_execution_id))
        self.agent_config = agent_config

    def handle(self, session, assistant_reply):
        assistant_reply = JsonCleaner.extract_json_array_section(assistant_reply)
        tasks = eval(assistant_reply)
        tasks = np.array(tasks).flatten().tolist()
        for task in reversed(tasks):
            self.task_queue.add_task(task)
        if len(tasks) > 0:
            logger.info("Adding task to queue: " + str(tasks))
        agent_execution = AgentExecution.find_by_id(session, self.agent_execution_id)
        for task in tasks:
            agent_execution_feed = AgentExecutionFeed(agent_execution_id=self.agent_execution_id,
                                                      agent_id=self.agent_config["agent_id"],
                                                      feed="New Task Added: " + task,
                                                      role="system",
                                                      feed_group_id=agent_execution.current_feed_group_id)
            session.add(agent_execution_feed)
        status = "COMPLETE" if len(self.task_queue.get_tasks()) == 0 else "PENDING"
        session.commit()
        return TaskExecutorResponse(status=status, retry=False)


class ReplaceTaskOutputHandler:
    """Handles the replace/prioritize task output type.
    Output is mostly in the array of tasks and handler adds every task to the task queue.
    """

    def __init__(self, agent_execution_id: int, agent_config: dict):
        self.agent_execution_id = agent_execution_id
        self.task_queue = TaskQueue(str(agent_execution_id))
        self.agent_config = agent_config

    def handle(self, session, assistant_reply):
        assistant_reply = JsonCleaner.extract_json_array_section(assistant_reply)
        tasks = eval(assistant_reply)
        self.task_queue.clear_tasks()
        for task in reversed(tasks):
            self.task_queue.add_task(task)
        if len(tasks) > 0:
            logger.info("Tasks reprioritized in order: " + str(tasks))
        status = "COMPLETE" if len(self.task_queue.get_tasks()) == 0 else "PENDING"
        session.commit()
        return TaskExecutorResponse(status=status, retry=False)


def get_output_handler(output_type: str, agent_execution_id: int, agent_config: dict, agent_tools: list = [],memory=None):
    if output_type == "tools":
        return ToolOutputHandler(agent_execution_id, agent_config, agent_tools,memory=memory)
    elif output_type == "replace_tasks":
        return ReplaceTaskOutputHandler(agent_execution_id, agent_config)
    elif output_type == "tasks":
        return TaskOutputHandler(agent_execution_id, agent_config)
    return ToolOutputHandler(agent_execution_id, agent_config, agent_tools,memory=memory)
