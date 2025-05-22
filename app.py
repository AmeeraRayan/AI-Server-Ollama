import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import json
app = FastAPI()

# Enable CORS so the UI EC2 can call this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict later
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate_outfit(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    full_prompt = (
        f"Give me exactly 3 outfit suggestions for: {prompt}. "
        "Each outfit must be numbered. Format: 1. ..., 2. ..., 3. "
        "Return everything in one response, not as a stream."
    )
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "tinyllama", "prompt": full_prompt},
            timeout=60
        )
        final_text = response.json().get("response","")
        print("MODEL RAW RESPONSE:", final_text)
        return {"response": final_text}

    except Exception as e:
        return {"error": str(e)}