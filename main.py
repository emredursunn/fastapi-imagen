from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os

# Google API key ortam değişkeninden alınır
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

@app.get("/generate")
def generate(prompt: str = Query("Fuzzy bunnies in my kitchen")):
    client = genai.Client()
    response = client.models.generate_images(
        model='imagen-3.0-generate-002',
        prompt=prompt,
        config=types.GenerateImagesConfig(number_of_images=1),
    )
    
    image_bytes = response.generated_images[0].image.image_bytes
    return StreamingResponse(BytesIO(image_bytes), media_type="image/png")
