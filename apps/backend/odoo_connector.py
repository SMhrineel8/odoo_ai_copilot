import xmlrpc.client
import os
from datetime import datetime

# -- Load Environment Variables Safely --
ODOO_URL = os.getenv("ODOO_URL", "").strip()
ODOO_DB = os.getenv("ODOO_DB", "").strip()
ODOO_USER = os.getenv("ODOO_USER", "").strip()
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD", "").strip()

# -- Validate Configuration --
required = {
    "ODOO_URL": ODOO_URL,
    "ODOO_DB": ODOO_DB,
    "ODOO_USER": ODOO_USER,
    "ODOO_PASSWORD": ODOO_PASSWORD
}

missing = [k for k, v in required.items() if not v]
if missing:
    raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")


# -- Connect to Odoo XML-RPC --
def get_client():
    try:
        common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
        uid = common.authenticate(ODOO_DB, ODOO_USER, ODOO_PASSWORD, {})
        if not uid:
            raise RuntimeError("Authentication failed. Check Odoo credentials.")
        models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")
        return uid, models
    except Exception as e:
        raise RuntimeError(f"Failed to connect to Odoo: {str(e)}")


# -----------------------------
# 🔹 Fetch Invoices
# -----------------------------
def fetch_invoices(limit=10):
    uid, models = get_client()
    domain = [['move_type', '=', 'out_invoice']]
    fields = ['name', 'amount_total', 'invoice_date']
    try:
        return models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'account.move', 'search_read',
            [domain], {'fields': fields, 'limit': limit}
        )
    except Exception as e:
        raise RuntimeError(f"Error fetching invoices: {str(e)}")


# -----------------------------
# 🔹 Fetch Low-Stock Inventory
# -----------------------------
def fetch_inventory(limit=10):
    uid, models = get_client()
    domain = [['quantity', '<', 10]]  # example: low stock threshold
    fields = ['product_id', 'quantity', 'location_id']
    try:
        return models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'stock.quant', 'search_read',
            [domain], {'fields': fields, 'limit': limit}
        )
    except Exception as e:
        raise RuntimeError(f"Error fetching inventory: {str(e)}")


# -----------------------------
# 🔹 Fetch Sales History
# -----------------------------
def fetch_sales_history(months=3):
    uid, models = get_client()
    try:
        today = datetime.today()
        # Shift months backwards
        month = today.month - months
        year = today.year
        if month <= 0:
            month += 12
            year -= 1
        start_date = datetime(year, month, 1).strftime('%Y-%m-%d')

        domain = [['date_order', '>=', start_date]]
        fields = ['date_order', 'amount_total']
        return models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'sale.order', 'search_read',
            [domain], {'fields': fields}
        )
    except Exception as e:
        raise RuntimeError(f"Error fetching sales history: {str(e)}")
