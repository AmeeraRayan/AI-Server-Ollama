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

    full_prompt = (f"Give me exactly 3 outfit ideas for a girl for: {prompt}. "
                   f" Each outfit must be clearly numbered and described briefly. Format: "
                   f"1. ... , 2. ... , 3. ..."
                   f"Please make sure the suggestions are stylish, practical, and easy to visualize.."
                   f"")

    try:
        output = subprocess.check_output([
            "/usr/local/bin/ollama", "run", "gemma:2b", full_prompt
        ]).decode("utf-8")
    except Exception as e:
        return {"error": str(e)}

    return {"response": output}