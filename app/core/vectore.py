from pinecone import Pinecone
from app.core.config import settings
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class VectorStore:
    def __init__(self):
        """Initialize Pinecone vector store connection"""
        try:
            self.pinecone = Pinecone(api_key=settings.PINECONE_API_KEY)
            self.index = self.pinecone.Index(settings.PINECONE_INDEX_NAME)
            logger.info("Pinecone vector store initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Pinecone: {e}")
            raise e
    
    def init_pinecone(self):
        """Initialize and return Pinecone client"""
        try:
            return self.pinecone
        except Exception as e:
            logger.error(f"Error initializing Pinecone: {e}")
            return None
    
    def create_index(self, index_name: str, dimension: int = 1536, metric: str = "cosine"):
        """Create a new Pinecone index"""
        try:
            if index_name not in [index.name for index in self.pinecone.list_indexes()]:
                self.pinecone.create_index(
                    name=index_name,
                    dimension=dimension,
                    metric=metric
                )
                logger.info(f"Index '{index_name}' created successfully")
                return True
            else:
                logger.info(f"Index '{index_name}' already exists")
                return True
        except Exception as e:
            logger.error(f"Error creating index: {e}")
            return False
    
    def upsert_vectors(self, vectors: List[Dict[str, Any]], namespace: str = ""):
        """Upsert vectors to the index"""
        try:
            result = self.index.upsert(vectors=vectors, namespace=namespace)
            logger.info(f"Upserted {len(vectors)} vectors successfully")
            return result
        except Exception as e:
            logger.error(f"Error upserting vectors: {e}")
            return None
    
    def query_vectors(self, 
                     query_vector: List[float], 
                     top_k: int = 10, 
                     namespace: str = "",
                     include_metadata: bool = True,
                     filter: Optional[Dict[str, Any]] = None):
        """Query similar vectors from the index"""
        try:
            result = self.index.query(
                vector=query_vector,
                top_k=top_k,
                namespace=namespace,
                include_metadata=include_metadata,
                filter=filter
            )
            logger.info(f"Query returned {len(result.matches)} matches")
            return result
        except Exception as e:
            logger.error(f"Error querying vectors: {e}")
            return None
    
    def delete_vectors(self, ids: List[str], namespace: str = ""):
        """Delete vectors by IDs"""
        try:
            result = self.index.delete(ids=ids, namespace=namespace)
            logger.info(f"Deleted {len(ids)} vectors successfully")
            return result
        except Exception as e:
            logger.error(f"Error deleting vectors: {e}")
            return None
    
    def get_stats(self, namespace: str = ""):
        """Get index statistics"""
        try:
            stats = self.index.describe_index_stats()
            return stats
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return None
    
    def list_namespaces(self):
        """List all namespaces in the index"""
        try:
            stats = self.get_stats()
            if stats and hasattr(stats, 'namespaces'):
                return list(stats.namespaces.keys())
            return []
        except Exception as e:
            logger.error(f"Error listing namespaces: {e}")
            return []
    
    def delete_namespace(self, namespace: str):
        """Delete all vectors in a namespace"""
        try:
            result = self.index.delete(delete_all=True, namespace=namespace)
            logger.info(f"Deleted namespace '{namespace}' successfully")
            return result
        except Exception as e:
            logger.error(f"Error deleting namespace: {e}")
            return None


# Global instance
vector_store = VectorStore()
