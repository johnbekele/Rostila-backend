import fastapi
from fastapi import Depends
from app.services.genai_service import GenaiService
from app.schemas.genai import GenaiRequest, GenaiResponse

router = fastapi.APIRouter()

def get_genai_service() -> GenaiService:
    return GenaiService()

@router.post("/generate-response")
async def generate_response(
    request: GenaiRequest,
    genai_service: GenaiService = Depends(get_genai_service)
    ):
    print(f"request: {request}")
    return genai_service.generate_response(request)