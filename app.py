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
        output = subprocess.check_output([
            "/usr/local/bin/ollama", "run", "tinyllama", full_prompt
        ]).decode("utf-8")
    except Exception as e:
        return {"error": str(e)}

    return {"response": output}