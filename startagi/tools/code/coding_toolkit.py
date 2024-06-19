from abc import ABC
from typing import List

from startagi.tools.base_tool import BaseToolkit, BaseTool, ToolConfiguration
from startagi.tools.code.improve_code import ImproveCodeTool
from startagi.tools.code.write_code import CodingTool
from startagi.tools.code.write_spec import WriteSpecTool
from startagi.tools.code.write_test import WriteTestTool


class CodingToolkit(BaseToolkit, ABC):
    name: str = "CodingToolkit"
    description: str = "Coding Tool kit contains all tools related to coding tasks"

    def get_tools(self) -> List[BaseTool]:
        return [CodingTool(), WriteSpecTool(), WriteTestTool(), ImproveCodeTool()]

    def get_env_keys(self) -> List[ToolConfiguration]:
        return []
