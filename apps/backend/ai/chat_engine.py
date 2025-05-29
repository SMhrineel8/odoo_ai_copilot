import os
import openai
from odoo_connector import fetch_invoices, fetch_inventory

# Load OpenAI key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY must be set")
openai.api_key = OPENAI_API_KEY

SYSTEM_PROMPT = (
    "You are an AI assistant for Odoo ERP. "
    "Use the provided data and answer user queries concisely."
)

def format_records(records):
    # Simplify list of dicts into a string
    out = []
    for r in records:
        parts = [f"{k}: {v}" for k, v in r.items() if v]
        out.append(" | ".join(parts))
    return "\n".join(out) or "No records found."

def chat_to_erp(user_query: str) -> str:
    # Pull data for context
    inv = fetch_invoices(limit=5)
    stock = fetch_inventory(limit=5)

    context = (
        f"Latest invoices:\n{format_records(inv)}\n\n"
        f"Low stock items:\n{format_records(stock)}\n\n"
        f"User asks: {user_query}"
    )

    resp = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": context}
        ],
        max_tokens=200,
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()
