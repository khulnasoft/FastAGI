import unittest
from unittest.mock import patch, MagicMock
from fastagi.types.vector_store_types import VectorStoreType
from fastagi.vector_store.pinecone import Pinecone
from fastagi.vector_store.weaviate import Weaviate
from fastagi.vector_store.qdrant import Qdrant
from fastagi.vector_store.vector_factory import VectorFactory
import pinecone
import weaviate


class MockPineconeIndex(pinecone.index.Index):
    pass


class MockWeaviate(Weaviate):
    pass


class MockQdrant(Qdrant):
    pass


class TestVectorFactory(unittest.TestCase):

    @patch('fastagi.vector_store.vector_factory.get_config')
    @patch('fastagi.vector_store.vector_factory.pinecone')
    @patch('fastagi.vector_store.vector_factory.weaviate')
    @patch('fastagi.vector_store.vector_factory.Qdrant')
    def test_get_vector_storage(self, mock_qdrant, mock_weaviate, mock_pinecone, mock_get_config):
        mock_get_config.return_value = 'test'
        mock_embedding_model = MagicMock()
        mock_embedding_model.get_embedding.return_value = [0.1, 0.2, 0.3]

        # Mock Pinecone index
        mock_pinecone_index = MockPineconeIndex('test_index')
        mock_pinecone.Index.return_value = mock_pinecone_index

        # Test Pinecone
        mock_pinecone.list_indexes.return_value = ['test_index']
        vector_store = VectorFactory.get_vector_storage(VectorStoreType.PINECONE, 'test_index', mock_embedding_model)
        self.assertIsInstance(vector_store, Pinecone)

        # Mock Weaviate client
        mock_weaviate_client = MagicMock()
        mock_weaviate.create_weaviate_client.return_value = mock_weaviate_client
        mock_weaviate.Weaviate = MockWeaviate

        # Test Weaviate
        vector_store = VectorFactory.get_vector_storage(VectorStoreType.WEAVIATE, 'test_index', mock_embedding_model)
        self.assertIsInstance(vector_store, Weaviate)

        # Test Qdrant
        mock_qdrant_client = MagicMock()
        mock_qdrant.create_qdrant_client.return_value = mock_qdrant_client
        mock_qdrant.Qdrant = MockQdrant

        vector_store = VectorFactory.get_vector_storage(VectorStoreType.QDRANT, 'test_index', mock_embedding_model)
        self.assertIsInstance(vector_store, Qdrant)

        # Test unsupported vector store
        with self.assertRaises(ValueError):
            VectorFactory.get_vector_storage(VectorStoreType.get_vector_store_type('Unsupported'), 'test_index',
                                             mock_embedding_model)


if __name__ == '__main__':
    unittest.main()
