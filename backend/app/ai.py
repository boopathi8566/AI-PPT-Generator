import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def generate_slides(notes):
    prompt = f"""
You are an AI presentation generator.

Convert the user's notes into a clear PowerPoint presentation.

User notes:
{notes}

Return ONLY valid JSON in this exact structure:

{{
    "title": "Presentation Title",
    "slides": [
        {{
            "slide_number": 1,
            "title": "Slide Title",
            "content": [
                "Point 1",
                "Point 2",
                "Point 3"
            ]
        }}
    ]
}}

Rules:
- Create 5 to 8 slides.
- Each slide should have a clear title.
- Each slide should contain 3 to 5 short points.
- Keep the content simple and presentation-friendly.
- Do not use markdown.
- Return JSON only.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    result = response.text.strip()

    # Remove markdown code fences if Gemini adds them
    if result.startswith("```"):
        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

    return json.loads(result)


if __name__ == "__main__":
    test_notes = """
    Food Delivery System.
    It connects customers with restaurants.
    Users can browse restaurants and order food.
    It supports digital payments and order tracking.
    """

    presentation = generate_slides(test_notes)

    print(json.dumps(presentation, indent=4))