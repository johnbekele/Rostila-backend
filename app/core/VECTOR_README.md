# Pinecone Vector Store Setup

This document explains how to set up and use the Pinecone vector database integration.

## Environment Variables

Add these environment variables to your `.env` file:

```env
# Pinecone Vector Store Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=your_pinecone_index_name_here
```

## Getting Started

1. **Get Pinecone API Key**: 
   - Sign up at [pinecone.io](https://pinecone.io)
   - Create a new project
   - Get your API key from the dashboard

2. **Create an Index**:
   - In Pinecone dashboard, create a new index
   - Recommended settings:
     - Dimension: 1536 (for OpenAI embeddings)
     - Metric: cosine
     - Pod type: p1 (for development)

3. **Set Environment Variables**:
   - Copy the API key and index name to your `.env` file

## Usage Examples

### Basic Vector Operations

```python
from app.core.vectore import vector_store

# Create an index
vector_store.create_index("my-index", dimension=1536, metric="cosine")

# Upsert vectors
vectors = [
    {
        "id": "doc1",
        "values": [0.1, 0.2, 0.3, ...],  # 1536-dimensional vector
        "metadata": {"text": "Sample document", "category": "example"}
    }
]
vector_store.upsert_vectors(vectors, namespace="documents")

# Query similar vectors
query_vector = [0.1, 0.2, 0.3, ...]  # 1536-dimensional vector
results = vector_store.query_vectors(
    query_vector=query_vector,
    top_k=5,
    namespace="documents"
)

# Delete vectors
vector_store.delete_vectors(["doc1"], namespace="documents")
```

### API Endpoints

The vector store is exposed via REST API endpoints:

- `POST /api/vector/upsert` - Upsert vectors
- `POST /api/vector/query` - Query similar vectors
- `POST /api/vector/delete` - Delete vectors
- `POST /api/vector/index/create` - Create index
- `GET /api/vector/stats` - Get index statistics
- `GET /api/vector/namespaces` - List namespaces
- `DELETE /api/vector/namespace/{namespace}` - Delete namespace
- `GET /api/vector/health` - Health check

### Example API Usage

```bash
# Health check
curl http://localhost:8000/api/vector/health

# Query vectors
curl -X POST http://localhost:8000/api/vector/query \
  -H "Content-Type: application/json" \
  -d '{
    "query_vector": [0.1, 0.2, 0.3],
    "top_k": 5,
    "namespace": "documents"
  }'
```

## Features

- ✅ Vector upsert (insert/update)
- ✅ Vector similarity search
- ✅ Vector deletion
- ✅ Index creation and management
- ✅ Namespace support
- ✅ Metadata filtering
- ✅ Statistics and monitoring
- ✅ Error handling and logging
- ✅ REST API endpoints

## Dependencies

The vector store requires:
- `pinecone-client==6.0.0` (already in requirements.txt)
- Valid Pinecone API key and index name

## Error Handling

All operations include comprehensive error handling and logging. Check the application logs for detailed error messages if operations fail.
