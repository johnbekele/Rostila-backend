# app/services/genai_service.py
from app.core.config import settings
from app.schemas.genai_schema import GenaiRequest, GenaiResponse
from google import genai
from google.genai.errors import ClientError

class GenaiService:
    def __init__(self):
        if not settings.GOOGLE_API_KEY:
            raise ValueError("Google API key not configured")
        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        
        # Coffee data context
        coffee_data = """Available Coffee Products:

ID: coffee-001
Name: Ethiopian Yirgacheffe G1
Origin: Yirgacheffe, Ethiopia (Sidamo)
Price: €45.00 (€15.00 per kg)
Rating: 4.8/5 (127 reviews)
Processing: Washed
Altitude: 1,800-2,200m
Flavor Notes: Floral, Citrus, Tea-like, Jasmine
Availability: In Stock (150 kg)
Producer: Abebe Coffee Farm
Certification: Organic
Cupping Score: 87.5/100
Description: Premium washed Yirgacheffe with exceptional floral notes and bright acidity.
Shipping Time: 2-3 weeks
Minimum Order: 50 kg
---

ID: coffee-002
Name: Ethiopian Sidamo Natural
Origin: Sidamo, Ethiopia (Sidamo)
Price: €42.00 (€14.00 per kg)
Rating: 4.6/5 (89 reviews)
Processing: Natural
Altitude: 1,600-1,900m
Flavor Notes: Berry, Chocolate, Wine, Fruity
Availability: In Stock (200 kg)
Producer: Kebede Family Farm
Certification: Fair Trade
Cupping Score: 85.0/100
Description: Rich natural processed Sidamo with intense berry flavors and wine-like acidity.
Shipping Time: 2-3 weeks
Minimum Order: 30 kg
---

ID: coffee-003
Name: Ethiopian Harrar Longberry
Origin: Harrar, Ethiopia (Harrar)
Price: €38.00 (€12.67 per kg)
Rating: 4.4/5 (156 reviews)
Processing: Natural
Altitude: 1,500-2,100m
Flavor Notes: Blueberry, Spice, Wine, Chocolate
Availability: Limited (75 kg)
Producer: Harrar Coffee Cooperative
Certification: Organic
Cupping Score: 83.5/100
Description: Classic Harrar with distinctive blueberry notes and wine-like characteristics.
Shipping Time: 3-4 weeks
Minimum Order: 25 kg
---

ID: coffee-004
Name: Ethiopian Guji Natural
Origin: Guji, Ethiopia (Guji)
Price: €48.00 (€16.00 per kg)
Rating: 4.9/5 (203 reviews)
Processing: Natural
Altitude: 1,900-2,300m
Flavor Notes: Strawberry, Mango, Tropical, Sweet
Availability: In Stock (120 kg)
Producer: Guji Highland Coffee
Certification: Organic, Fair Trade
Cupping Score: 89.0/100
Description: Exceptional Guji natural with tropical fruit notes and exceptional sweetness.
Shipping Time: 2-3 weeks
Minimum Order: 40 kg
---

ID: coffee-005
Name: Ethiopian Limu Washed
Origin: Limu, Ethiopia (Limu)
Price: €41.00 (€13.67 per kg)
Rating: 4.5/5 (94 reviews)
Processing: Washed
Altitude: 1,400-2,000m
Flavor Notes: Lemon, Herbal, Clean, Bright
Availability: In Stock (180 kg)
Producer: Limu Coffee Union
Certification: Fair Trade
Cupping Score: 84.5/100
Description: Clean washed Limu with bright citrus notes and herbal undertones.
Shipping Time: 2-3 weeks
Minimum Order: 35 kg
---

ID: coffee-006
Name: Ethiopian Jimma Organic
Origin: Jimma, Ethiopia (Jimma)
Price: €39.00 (€13.00 per kg)
Rating: 4.3/5 (67 reviews)
Processing: Semi-washed
Altitude: 1,300-1,800m
Flavor Notes: Nutty, Chocolate, Mild, Balanced
Availability: In Stock (250 kg)
Producer: Jimma Organic Cooperative
Certification: Organic
Cupping Score: 82.0/100
Description: Balanced organic Jimma with nutty chocolate notes and mild acidity.
Shipping Time: 2-3 weeks
Minimum Order: 50 kg
---

ID: coffee-007
Name: Ethiopian Kochere Washed
Origin: Kochere, Ethiopia (Yirgacheffe)
Price: €46.00 (€15.33 per kg)
Rating: 4.7/5 (145 reviews)
Processing: Washed
Altitude: 1,800-2,200m
Flavor Notes: Floral, Lemon, Tea, Elegant
Availability: In Stock (90 kg)
Producer: Kochere Coffee Farm
Certification: Organic, Fair Trade
Cupping Score: 86.5/100
Description: Elegant washed Kochere with delicate floral notes and tea-like finish.
Shipping Time: 2-3 weeks
Minimum Order: 30 kg
---

ID: coffee-008
Name: Ethiopian Gedeb Natural
Origin: Gedeb, Ethiopia (Yirgacheffe)
Price: €44.00 (€14.67 per kg)
Rating: 4.6/5 (112 reviews)
Processing: Natural
Altitude: 1,700-2,100m
Flavor Notes: Strawberry, Wine, Fruity, Complex
Availability: Limited (60 kg)
Producer: Gedeb Coffee Collective
Certification: Organic
Cupping Score: 85.5/100
Description: Complex natural Gedeb with strawberry wine notes and layered complexity.
Shipping Time: 3-4 weeks
Minimum Order: 25 kg
---"""

        # Updated context with coffee data
        self.context = (
            "You are a helpful coffee expert assistant for Rostila Coffee. "
            "you are create and trained by John Bekele .Lead devloper for the project "
            "You have access to our complete coffee inventory and can help customers with: "
            "coffee recommendations, flavor profiles, pricing, availability, shipping information, "
            "and general coffee knowledge. "
            f"\n\n{coffee_data}\n\n"
            "Always respond ONLY in JSON format. "
            "Do NOT ask for more information. "
            "if client insiste to specifice answer say plase reach out to my developer John Bekele for more information"
            "Use this format: "
            "{'message': '<personalized message>', 'schedule': [{'time': '<time>', 'todo': '<task>'}, ...]}"
        )

    def generate_response(self, request: GenaiRequest) -> GenaiResponse:
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