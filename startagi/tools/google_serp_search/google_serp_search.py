from typing import Type, Optional, Any
from pydantic import BaseModel, Field
import aiohttp
from fastagi.helper.error_handler import ErrorHandler
from fastagi.helper.google_serp import GoogleSerpApiWrap
from fastagi.llms.base_llm import BaseLlm
from fastagi.models.agent_execution import AgentExecution
from fastagi.models.agent_execution_feed import AgentExecutionFeed
from fastagi.tools.base_tool import BaseTool
import os

import json


class GoogleSerpSchema(BaseModel):
    query: str = Field(
        ...,
        description="The search query for Google SERP.",
    )


'''Google search using serper.dev. Use server.dev api keys'''
class GoogleSerpTool(BaseTool):
    """
    Google Search tool

    Attributes:
        name : The name.
        description : The description.
        args_schema : The args schema.
    """
    llm: Optional[BaseLlm] = None
    name = "GoogleSerp"
    agent_id: int = None
    agent_execution_id: int = None
    description = (
        "A tool for performing a Google SERP search and extracting snippets and webpages."
        "Input should be a search query."
    )
    args_schema: Type[GoogleSerpSchema] = GoogleSerpSchema

    class Config:
        arbitrary_types_allowed = True

    def _execute(self, query: str) -> tuple:
        """
        Execute the Google search tool.

        Args:
            query : The query to search for.

        Returns:
            Search result summary along with related links
        """
        api_key = self.get_tool_config("SERP_API_KEY")
        serp_api = GoogleSerpApiWrap(api_key)
        response = serp_api.search_run(query)
        summary = self.summarise_result(query, response["snippets"])
        if response["links"]:
            return summary + "\n\nLinks:\n" + "\n".join("- " + link for link in response["links"][:3])
        return summary

    def summarise_result(self, query, snippets):
        summarize_prompt = """Summarize the following text `{snippets}`
            Write a concise or as descriptive as necessary and attempt to
            answer the query: `{query}` as best as possible. Use markdown formatting for
            longer responses."""

        summarize_prompt = summarize_prompt.replace("{snippets}", str(snippets))
        summarize_prompt = summarize_prompt.replace("{query}", query)

        messages = [{"role": "system", "content": summarize_prompt}]
        result = self.llm.chat_completion(messages, max_tokens=self.max_token_limit)
        
        if 'error' in result and result['message'] is not None:
            ErrorHandler.handle_openai_errors(self.toolkit_config.session, self.agent_id, self.agent_execution_id, result['message'])
        return result["content"]
