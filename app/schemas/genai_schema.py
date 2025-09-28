from pydantic import BaseModel
from typing import List, Dict ,Optional


class GenaiRequest(BaseModel):
    prompt: str
    username: str


class GenaiResponse(BaseModel):
    response: Optional[dict | list |List[dict]]