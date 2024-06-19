from abc import ABC
from typing import List
from startagi.tools.base_tool import BaseTool, BaseToolkit, ToolConfiguration
from startagi.tools.thinking.tools import ThinkingTool
from startagi.types.key_type import ToolConfigKeyType


class ThinkingToolkit(BaseToolkit, ABC):
    name: str = "Thinking Toolkit"
    description: str = "Toolkit containing tools for intelligent problem-solving"

    def get_tools(self) -> List[BaseTool]:
        return [
            ThinkingTool(),
        ]

    def get_env_keys(self) -> List[ToolConfiguration]:
        return []
