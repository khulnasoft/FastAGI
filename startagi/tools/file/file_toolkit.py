from abc import ABC
from typing import List
from startagi.tools.base_tool import BaseTool, BaseToolkit, ToolConfiguration
from startagi.tools.file.append_file import AppendFileTool
from startagi.tools.file.delete_file import DeleteFileTool
from startagi.tools.file.list_files import ListFileTool
from startagi.tools.file.read_file import ReadFileTool
from startagi.tools.file.write_file import WriteFileTool
from startagi.types.key_type import ToolConfigKeyType
from startagi.models.tool_config import ToolConfig


class FileToolkit(BaseToolkit, ABC):
    name: str = "File Toolkit"
    description: str = "File Tool kit contains all tools related to file operations"

    def get_tools(self) -> List[BaseTool]:
        return [AppendFileTool(), DeleteFileTool(), ListFileTool(), ReadFileTool(), WriteFileTool()]

    def get_env_keys(self) -> List[ToolConfiguration]:
        return []
