"""
Example usage of the Pinecone Vector Store
This file demonstrates how to use the VectorStore class for common operations
"""

from app.core.vectore import vector_store
import numpy as np
from typing import List, Dict, Any

def example_usage():
    """Example demonstrating vector store operations"""
    
    # 1. Create an index (if it doesn't exist)
    print("Creating index...")
    success = vector_store.create_index(
        index_name="example-index",
        dimension=1536,  # OpenAI embedding dimension
        metric="cosine"
    )
    print(f"Index creation: {'Success' if success else 'Failed'}")
    
    # 2. Prepare sample vectors
    sample_vectors = [
        {
            "id": "vec1",
            "values": np.random.rand(1536).tolist(),
            "metadata": {"text": "This is a sample document about AI", "category": "technology"}
        },
        {
            "id": "vec2", 
            "values": np.random.rand(1536).tolist(),
            "metadata": {"text": "Another document about machine learning", "category": "technology"}
        },
        {
            "id": "vec3",
            "values": np.random.rand(1536).tolist(), 
            "metadata": {"text": "A document about cooking recipes", "category": "food"}
        }
    ]
    
    # 3. Upsert vectors
    print("\nUpserting vectors...")
    result = vector_store.upsert_vectors(sample_vectors, namespace="examples")
    print(f"Upsert result: {result}")
    
    # 4. Query similar vectors
    print("\nQuerying similar vectors...")
    query_vector = np.random.rand(1536).tolist()
    query_result = vector_store.query_vectors(
        query_vector=query_vector,
        top_k=2,
        namespace="examples",
        include_metadata=True
    )
    
    if query_result:
        print(f"Found {len(query_result.matches)} similar vectors:")
        for match in query_result.matches:
            print(f"  ID: {match.id}, Score: {match.score:.4f}")
            print(f"  Metadata: {match.metadata}")
    
    # 5. Get index statistics
    print("\nIndex statistics:")
    stats = vector_store.get_stats()
    if stats:
        print(f"Total vectors: {stats.total_vector_count}")
        print(f"Namespaces: {list(stats.namespaces.keys()) if hasattr(stats, 'namespaces') else 'None'}")
    
    # 6. List namespaces
    print("\nAvailable namespaces:")
    namespaces = vector_store.list_namespaces()
    print(f"Namespaces: {namespaces}")
    
    # 7. Delete specific vectors
    print("\nDeleting vectors...")
    delete_result = vector_store.delete_vectors(["vec1", "vec2"], namespace="examples")
    print(f"Delete result: {delete_result}")
    
    # 8. Clean up - delete namespace
    print("\nCleaning up namespace...")
    cleanup_result = vector_store.delete_namespace("examples")
    print(f"Namespace cleanup: {'Success' if cleanup_result else 'Failed'}")

if __name__ == "__main__":
    example_usage()
