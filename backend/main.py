from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FREEPIK_API_KEY = os.getenv("FREEPIK_API_KEY")
FREEPIK_API_URL = "https://api.freepik.com/v1/ai/text-to-image"

class GenerateRequest(BaseModel):
    text: str

@app.post("/generate")
async def generate_image(request: GenerateRequest):
    if not FREEPIK_API_KEY:
        raise HTTPException(status_code=500, detail="FREEPIK_API_KEY not set in .env")

    headers = {
        "x-freepik-api-key": FREEPIK_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": request.text,
        "image": {
            "size": "square_1_1"  # 1:1 aspect ratio
        }
    }

    try:
        # Submit image generation request
        response = requests.post(FREEPIK_API_URL, headers=headers, json=payload)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, 
                detail=f"Freepik API error: {response.text}"
            )
        
        result = response.json()
        
        # Freepik API is asynchronous, need to poll for result
        # The response contains a task that we need to check
        if "data" in result and len(result["data"]) > 0:
            image_data = result["data"][0]
            
            # If the image is immediately available (base64)
            if "base64" in image_data:
                return {"image": image_data["base64"]}
            
            # If we have a URL to the generated image
            elif "url" in image_data:
                # Download the image and convert to base64
                img_response = requests.get(image_data["url"])
                if img_response.status_code == 200:
                    img_base64 = base64.b64encode(img_response.content).decode("utf-8")
                    return {"image": img_base64}
        
        raise HTTPException(status_code=500, detail="Unexpected response format from Freepik API")
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")
