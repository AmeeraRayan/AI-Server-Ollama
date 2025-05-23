# AI-Server-Ollama – AI Backend for Fashion Recommendation

This repository provides the backend AI server for the OllamaStylist project. It is responsible for processing user prompts and generating outfit suggestions using the Ollama LLM.

---

## Overview

This service acts as a FastAPI backend that receives user prompts from the UI server (Flask) and forwards them to an Ollama language model (like `tinyllama`). The model returns 3 outfit options, which are sent back to the UI.

- FastAPI handles the endpoint.
- Subprocess is used to run the Ollama model.
- Lightweight and efficient to isolate the model logic from UI code.
- Built-in response timing to monitor AI inference latency.

---

## Endpoint

### `POST /generate`

**Request body:**
```json
{
  "prompt": "What should I wear for a summer picnic?"
}
```

**Response:**
```json
{
  "response": "1. Light floral dress with sun hat, 2. Linen shorts with a tank top, 3. Casual jumpsuit with flat sandals"
}
```

---

## Architecture

The AI server runs on an EC2 instance inside a private subnet (10.0.1.0/24) and communicates with:

- **Flask UI** hosted on another EC2 in subnet 10.0.0.0/24
- **Ollama** (local model inference)
- **Hugging Face** (image generation after user selects an outfit)

### Request Flow:
```
User → Flask UI → FastAPI AI Server → Ollama → AI Server → UI → Hugging Face (if image requested)
```

---

## Tech Stack

| Component    | Technology         |
|--------------|--------------------|
| Backend      | FastAPI, Python    |
| AI Model     | Ollama (tinyllama) |
| Deployment   | Systemd, EC2, VPC  |
| Integration  | Flask UI, Hugging Face |

---

## Deployment

### 1. Edit the Service File
Make sure paths and user match your EC2 setup:
```bash
nano ai-server.service
```

### 2. Deploy the Server
```bash
bash deploy.sh
```

### 3. Check Status
```bash
sudo systemctl status ai-server.service
```

---

## Folder Structure

```
.
├── app.py                 # FastAPI server
├── deploy.sh              # Bash deployment script
├── ai-server.service      # Systemd service unit file
├── requirements.txt       # Python dependencies
└── .github/workflows/deploy.yaml  # GitHub Actions CI/CD
```

---

## Testing with Curl
```

During development, we used curl to manually test the FastAPI /generate endpoint and verify correct communication with the Ollama model.

Here’s an example command:

```bash
curl -X POST http://<AI_SERVER_IP>:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What should I wear for a summer picnic?"}'

```
This helped ensure that:
 • The prompt was correctly passed from the Flask app to the AI server.
 • The AI server successfully forwarded the prompt to Ollama (e.g., tinyllama).
 • A list of 3 outfit suggestions was returned as expected.

---
## License

MIT

---

## Created by

**Ameera Rayan** – Full-stack AI Developer  
GitHub: [AmeeraRayan](https://github.com/AmeeraRayan)
