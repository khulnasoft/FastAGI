from abc import ABC
from typing import List
from fastagi.tools.base_tool import BaseTool, BaseToolkit, ToolConfiguration
from fastagi.tools.file.append_file import AppendFileTool
from fastagi.tools.file.delete_file import DeleteFileTool
from fastagi.tools.file.list_files import ListFileTool
from fastagi.tools.file.read_file import ReadFileTool
from fastagi.tools.file.write_file import WriteFileTool
from fastagi.types.key_type import ToolConfigKeyType
from fastagi.models.tool_config import ToolConfig


class FileToolkit(BaseToolkit, ABC):
    name: str = "File Toolkit"
    description: str = "File Tool kit contains all tools related to file operations"

    def get_tools(self) -> List[BaseTool]:
        return [AppendFileTool(), DeleteFileTool(), ListFileTool(), ReadFileTool(), WriteFileTool()]

    def get_env_keys(self) -> List[ToolConfiguration]:
        return []
