from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.ai import generate_slides
from app.ppt_generator import create_presentation
import os

app = FastAPI(title="AI PPT Generator")
@app.get("/")
def serve_frontend():
    return FileResponse("index.html")


# Allow the frontend HTML to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PresentationRequest(BaseModel):
    notes: str
    theme: int = 0
    design: int = 0


@app.get("/")
def home():
    return {
        "message": "AI PPT Generator Backend is Running!"
    }


@app.get("/health")
def health():
    return {
        "status": "OK"
    }

@app.post("/generate-slides")
def generate_slide_content(request: PresentationRequest):
    # Generate slide content using Gemini AI
    presentation_data = generate_slides(request.notes)

    # Return AI-generated slide data for frontend preview
    return presentation_data

@app.post("/generate")
def generate_presentation(request: PresentationRequest):

    # Step 1: Generate slide content using Gemini AI
    presentation_data = generate_slides(request.notes)

    # Step 2: Create a writable temporary folder on Vercel
    output_folder = "/tmp/generated_ppt"
    os.makedirs(output_folder, exist_ok=True)

    # Step 3: Create PowerPoint file
    output_path = os.path.join(
        output_folder,
        "AI_Generated_Presentation.pptx"
    )

    create_presentation(
        presentation_data,
        output_path,
        request.theme,
        request.design
    )

    # Step 4: Return the PowerPoint file
    return FileResponse(
        output_path,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename="AI_Generated_Presentation.pptx"
    )