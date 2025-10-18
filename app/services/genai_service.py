 # app/services/genai_service.py
from fastapi import HTTPException , status
from app.core.config import settings
from app.schemas.genai_schema import GenaiRequest, GenaiResponse
from google import genai
from google.genai.errors import ClientError
from typing import List
import json
from  pathlib import Path 


class GenaiService:
    def __init__(self):
        if not settings.GOOGLE_API_KEY:
            raise ValueError("Google API key not configured")
        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        
        # Load coffee data from JSON file
        self.path = Path(__file__).parent.parent / "data" / "coffe_data.json"
        with self.path.open() as f:
            coffee_data_json = json.load(f)
        
        # Format coffee data for context
        self.coffee_data = json.dumps(coffee_data_json, indent=2)

        # Updated context with coffee data
        self.context = (
            "You are a helpful coffee expert assistant for Rostila Coffee. "
            "you are create and trained by John Bekele .Lead devloper for the project "
            "You have access to our complete coffee inventory and can help customers with: "
            "coffee recommendations, flavor profiles, pricing, availability, shipping information, "
            "and general coffee knowledge. "
            f"\n\n{self.coffee_data}\n\n"
            "Always respond ONLY in JSON format. "
            "Do NOT ask for more information. "
            "if client insiste to specifice answer say plase reach out to my developer John Bekele for more information"
            "Use this format: "
            "{'message': '<personalized message>'"
        )

    def generate_response(self, request: GenaiRequest) -> GenaiResponse:
        print(f"request: {self.coffee_data}")
        try:
            full_prompt = f"{self.context}\n\nUser: {request.prompt}\nUsername: {request.username}"
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[full_prompt]
            )

            # Remove code blocks if any
            clean_text = response.text.replace("```json", "").replace("```", "").strip()

            # Convert to dict
            import json
            data = json.loads(clean_text)
            return GenaiResponse(response=data)

        except Exception as e:
            return GenaiResponse(response={"message": f"Error: {e}", "schedule": []})

    def generate_embeddings(self, text: str) -> List[float]:
        try:
            embeddings = self.client.models.embed_content(
                model="text-embedding-004",
                 contents=[text])
            return embeddings.data[0].embedding
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"Error generating embeddings: {e}")
            return None