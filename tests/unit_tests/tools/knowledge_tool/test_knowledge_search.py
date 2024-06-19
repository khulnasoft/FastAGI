import unittest
from unittest.mock import Mock, patch
from startagi.tools.knowledge_search.knowledge_search import KnowledgeSearchTool
from pydantic.main import BaseModel

class TestKnowledgeSearchTool(unittest.TestCase):
    def setUp(self):
        self.tool = KnowledgeSearchTool()
        self.tool.toolkit_config = Mock(session=Mock())
        self.tool.agent_id = 1

    @patch('startagi.models.knowledges.Knowledges.get_knowledge_from_id')
    @patch('startagi.models.agent_config.AgentConfiguration')
    @patch('startagi.models.toolkit.Toolkit')
    @patch('startagi.models.vector_db_indices.VectordbIndices.get_vector_index_from_id')
    @patch('startagi.models.vector_dbs.Vectordbs.get_vector_db_from_id')
    @patch('startagi.models.vector_db_configs.VectordbConfigs.get_vector_db_config_from_db_id')
    @patch('startagi.models.configuration.Configuration.fetch_configuration')
    @patch('startagi.jobs.agent_executor.AgentExecutor.get_embedding')

    def test_execute(self, mock_get_embedding, mock_fetch_configuration, mock_get_vector_db_config_from_db_id, mock_get_vector_db_from_id, mock_get_vector_index_from_id, mock_Toolkit, mock_AgentConfiguration, mock_get_knowledge_from_id):
        mock_get_embedding.return_value = None
        mock_AgentConfiguration.filter.first.return_value = Mock(value=None)
        mock_get_knowledge_from_id.return_value = None
        result = self.tool._execute(query="test")
        self.assertEqual(result, "Selected Knowledge not found")
