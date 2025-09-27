# app/services/genai_service.py
from app.core.config import settings
from app.schemas.genai import GenaiRequest, GenaiResponse
from google import genai
from google.genai.errors import ClientError

class GenaiService:
    def __init__(self):
        if not settings.GOOGLE_API_KEY:
            raise ValueError("Google API key not configured")
        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        # Strong instruction to enforce JSON output
        self.context = (
            "You are a helpful assistant. "
            "Always respond ONLY in JSON format. "
            "Do NOT ask for more information. "
            "Use this format: "
            "{'message': '<personalized message>', 'schedule': [{'time': '<time>', 'todo': '<task>'}, ...]}"
        )

    def generate_response(self, request: GenaiRequest) -> GenaiResponse:
        try:
            full_prompt = f"{self.context}\n\nUser: {request.prompt}\nUsername: {request.username}"
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[full_prompt]  # make sure it’s a string in a list
            )

            # Remove code blocks if any
            clean_text = response.text.replace("```json", "").replace("```", "").strip()

            # Convert to dict
            import json
            data = json.loads(clean_text)
            return GenaiResponse(response=data)

        except Exception as e:
            return GenaiResponse(response={"message": f"Error: {e}", "schedule": []})
