from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import os
from ai.chat_engine import chat_to_erp
from odoo_connector import fetch_invoices, fetch_inventory

app = FastAPI(title="Odoo AI Copilot")

# Health check
@app.get("/health")
async def health():
    return {"status": "ok"}

# ---- Chat Interface ----
class ChatRequest(BaseModel):
    question: str

@app.post("/api/v1/chat")
async def api_chat(req: ChatRequest):
    try:
        answer = chat_to_erp(req.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---- Data Endpoints ----
@app.get("/api/v1/invoices")
async def api_invoices():
    return {"invoices": fetch_invoices(limit=10)}

@app.get("/api/v1/inventory")
async def api_inventory():
    return {"inventory": fetch_inventory(limit=10)}
