import sys
if 'google' in sys.modules:
    del sys.modules['google']

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from google import genai
from google.generativeai.types import GenerateImageRequest, GenerateImagesConfig
from io import BytesIO
from PIL import Image
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

@app.get("/generate")
def generate_image(prompt: str = "Fuzzy bunnies in my kitchen"):
    model = genai.GenerativeModel("imagen-3.0-generate-002")
    response = model.generate_images(
        prompt=prompt,
        config=GenerateImagesConfig(number_of_images=1),
    )
    img_data = response.generated_images[0].image.image_bytes
    return StreamingResponse(BytesIO(img_data), media_type="image/png")
