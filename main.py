from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from google import genai
from google.genai import types
import base64
import os

app = FastAPI()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.post("/generate-image")
async def generate_image(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "A happy bunny in a forest")

    model = genai.GenerativeModel(model_name="imagen-3.0-generate-002")
    try:
        response = model.generate_images(
            prompt=prompt,
            config=types.GenerateImagesConfig(number_of_images=1)
        )
        image_bytes = response.generated_images[0].image.image_bytes
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        return JSONResponse(content={"image": f"data:image/png;base64,{base64_image}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
