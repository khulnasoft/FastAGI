from unittest.mock import Mock

import pytest

from fastagi.tools.code.write_spec import WriteSpecTool
from unittest.mock import MagicMock


class MockBaseLlm:
    def chat_completion(self, messages, max_tokens):
        return {"content": "Generated specification"}

    def get_model(self):
        return "gpt-3.5-turbo"

class TestWriteSpecTool:

    @pytest.fixture
    def tool(self):
        tool = WriteSpecTool()
        tool.llm = MockBaseLlm()
        tool.resource_manager = Mock()
        mock_session = MagicMock(name="session")
        tool.toolkit_config.session = mock_session
        return tool

    def test_execute(self, tool):
        tool.resource_manager.write_file = Mock()
        tool.resource_manager.write_file.return_value = "File write successful"
        response = tool._execute("Test task description", "test_spec_file.txt")
        assert response == "Generated specification\nSpecification generated and saved successfully"
        tool.resource_manager.write_file.assert_called_once_with("test_spec_file.txt", "Generated specification")
