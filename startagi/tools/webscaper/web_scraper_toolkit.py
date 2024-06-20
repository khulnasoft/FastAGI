from abc import ABC
from typing import List
from fastagi.tools.base_tool import BaseTool, BaseToolkit, ToolConfiguration
from fastagi.tools.webscaper.tools import WebScraperTool
from fastagi.types.key_type import ToolConfigKeyType

class WebScrapperToolkit(BaseToolkit, ABC):
    name: str = "Web Scrapper Toolkit"
    description: str = "Web Scrapper tool kit is used to scrape web"

    def get_tools(self) -> List[BaseTool]:
        return [
            WebScraperTool(),
        ]

    def get_env_keys(self) -> List[ToolConfiguration]:
        return []
