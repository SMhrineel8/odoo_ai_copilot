from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import os
import openai
from odoo_connector import OdooConnector

app = FastAPI(title="Odoo AI Copilot Backend")

# Load OpenAI key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set")
openai.api_key = OPENAI_API_KEY

# Load Odoo credentials
ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USER = os.getenv("ODOO_USER")
ODOO_PASS = os.getenv("ODOO_PASS")
if not all([ODOO_URL, ODOO_DB, ODOO_USER, ODOO_PASS]):
    raise RuntimeError("Odoo connection vars missing")

# Dependency: one connector per request
def get_odoo():
    return OdooConnector(ODOO_URL, ODOO_DB, ODOO_USER, ODOO_PASS)

class PromptRequest(BaseModel):
    prompt: str
    max_tokens: int = 150

@app.get("/")
async def health():
    return {"status": "ok"}

@app.post("/api/v1/chat")
async def chat(request: PromptRequest):
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": request.prompt}],
            max_tokens=request.max_tokens,
            temperature=0.2,
        )
        return {"response": resp.choices[0].message.content.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/odoo/sales")
async def monthly_sales(odoo: OdooConnector = Depends(get_odoo)):
    """Fetch total sales for current month from Odoo"""
    total, records = odoo.fetch_monthly_sales()
    return {"total_sales": total, "records": records}
