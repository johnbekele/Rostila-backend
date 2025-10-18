from typing import List, Dict, Any, Optional
from beanie import Document
from app.core.vectore import vector_store
from app.repositories.base_repository import BaseRepository
from app.models.coffee import Coffee



class BaseVectoreRepository(BaseRepository):
    def __init__(self, model: type[Document]):
        super().__init__(model)

    async def create_vector(self, vector: Dict[str, Any]) -> Dict[str, Any]:
        return await vector_store.upsert_vectors(vector)
    
    async def get_vector(self, vector_id: str) -> Dict[str, Any]:
        return await vector_store.get_vector(vector_id)
    
    async def delete_vector(self, vector_id: str) -> Dict[str, Any]:
        return await vector_store.delete_vector(vector_id)