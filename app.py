import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import subprocess

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
    full_prompt = f"3 outfit ideas for: {prompt}. Format: 1. ... 2. ... 3."

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "tinyllama", "prompt": full_prompt},
            timeout=60
        )
        response.raise_for_status()
        lines = []
        for line in response.iter_lines():
            if line:
                lines.append(line.decode("utf-8"))
        return {"response": "\n".join(lines)}
    except Exception as e:
        return {"error": str(e)}