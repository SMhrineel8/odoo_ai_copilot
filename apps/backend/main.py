from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import openai

app = FastAPI(title="Odoo AI Copilot Backend")

# Load your OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY environment variable not set")
openai.api_key = OPENAI_API_KEY

class PromptRequest(BaseModel):
    prompt: str
    max_tokens: int = 150

@app.get("/")
async def root():
    return {"message": "Welcome to Odoo AI Copilot Backend!"}

@app.post("/generate")
async def generate_text(request: PromptRequest):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=0.7,
        )
        return {"response": response.choices[0].text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
