from abc import ABC
from typing import List

from startagi.tools.base_tool import BaseTool, BaseToolkit, ToolConfiguration
from startagi.tools.image_generation.dalle_image_gen import DalleImageGenTool
from startagi.tools.image_generation.stable_diffusion_image_gen import StableDiffusionImageGenTool
from startagi.types.key_type import ToolConfigKeyType

class ImageGenToolkit(BaseToolkit, ABC):
    name: str = "Image Generation Toolkit"
    description: str = "Toolkit containing a tool for generating images"

    def get_tools(self) -> List[BaseTool]:
        return [DalleImageGenTool(), StableDiffusionImageGenTool()]

    def get_env_keys(self) -> List[ToolConfiguration]:
        return [
            ToolConfiguration(key="STABILITY_API_KEY", key_type=ToolConfigKeyType.STRING, is_required=False, is_secret = True),
            ToolConfiguration(key="ENGINE_ID", key_type=ToolConfigKeyType.STRING, is_required=False, is_secret=False),
            ToolConfiguration(key="OPENAI_API_KEY", key_type=ToolConfigKeyType.STRING, is_required=False, is_secret=True)
        ]
