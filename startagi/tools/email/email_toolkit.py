from abc import ABC
from fastagi.tools.base_tool import BaseToolkit, BaseTool, ToolConfiguration
from typing import Type, List
from fastagi.tools.email.read_email import ReadEmailTool
from fastagi.tools.email.send_email import SendEmailTool
from fastagi.tools.email.send_email_attachment import SendEmailAttachmentTool
from fastagi.types.key_type import ToolConfigKeyType


class EmailToolkit(BaseToolkit, ABC):
    name: str = "Email Toolkit"
    description: str = "Email Tool kit contains all tools related to sending email"

    def get_tools(self) -> List[BaseTool]:
        return [ReadEmailTool(), SendEmailTool(), SendEmailAttachmentTool()]

    def get_env_keys(self) -> List[ToolConfiguration]:
        return [
            ToolConfiguration(key="EMAIL_ADDRESS", key_type=ToolConfigKeyType.STRING, is_required= True, is_secret = False),
            ToolConfiguration(key="EMAIL_PASSWORD", key_type=ToolConfigKeyType.STRING, is_required=True, is_secret=True),
            ToolConfiguration(key="EMAIL_SIGNATURE", key_type=ToolConfigKeyType.STRING, is_required=False, is_secret=False),
            ToolConfiguration(key="EMAIL_DRAFT_MODE", key_type=ToolConfigKeyType.STRING, is_required=True, is_secret=False),
            ToolConfiguration(key="EMAIL_DRAFT_FOLDER", key_type=ToolConfigKeyType.STRING, is_required=True, is_secret=False),
            ToolConfiguration(key="EMAIL_SMTP_HOST", key_type=ToolConfigKeyType.STRING, is_required=True, is_secret=False),
            ToolConfiguration(key="EMAIL_SMTP_PORT", key_type=ToolConfigKeyType.STRING, is_required=True, is_secret=False),
            ToolConfiguration(key="EMAIL_IMAP_SERVER", key_type=ToolConfigKeyType.STRING, is_required=True, is_secret=False)
        ]