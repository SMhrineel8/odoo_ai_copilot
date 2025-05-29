from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

# Internal imports
from ai.chat_engine import chat_to_erp
from odoo_connector import fetch_invoices, fetch_inventory

# Initialize FastAPI
app = FastAPI(
    title="Odoo AI Copilot",
    description="AI Copilot for Odoo, Zoho, Tally — Natural Language ERP Control",
    version="1.0.0"
)

# CORS settings (Allow frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check
@app.get("/health")
async def health():
    return {"status": "ok"}

# -----------------------------
# 🔹 Chat Endpoint
# -----------------------------

class ChatRequest(BaseModel):
    question: str

@app.post("/api/v1/chat")
async def api_chat(req: ChatRequest):
    try:
        answer = chat_to_erp(req.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")

# -----------------------------
# 🔹 Data Endpoints
# -----------------------------

@app.get("/api/v1/invoices")
async def api_invoices():
    try:
        return {"invoices": fetch_invoices(limit=10)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Invoice fetch failed: {str(e)}")

@app.get("/api/v1/inventory")
async def api_inventory():
    try:
        return {"inventory": fetch_inventory(limit=10)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inventory fetch failed: {str(e)}")
