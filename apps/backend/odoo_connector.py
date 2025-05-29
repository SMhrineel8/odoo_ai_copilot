import xmlrpc.client
import os
from datetime import datetime

# Load Odoo creds from env
ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USER = os.getenv("ODOO_USER")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")

if not all([ODOO_URL, ODOO_DB, ODOO_USER, ODOO_PASSWORD]):
    raise RuntimeError("ODOO_URL, ODOO_DB, ODOO_USER, and ODOO_PASSWORD must all be set")

def get_client():
    common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
    uid = common.authenticate(ODOO_DB, ODOO_USER, ODOO_PASSWORD, {})
    models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")
    return uid, models

def fetch_invoices(limit=10):
    uid, models = get_client()
    domain = [[['move_type', '=', 'out_invoice']]]
    fields = ['name', 'amount_total', 'invoice_date']
    return models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'account.move', 'search_read',
                             domain, {'fields': fields, 'limit': limit})

def fetch_inventory(limit=10):
    uid, models = get_client()
    domain = [[['quantity', '<', 10]]]  # low stock example
    fields = ['product_id', 'quantity', 'location_id']
    return models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'stock.quant', 'search_read',
                             domain, {'fields': fields, 'limit': limit})

def fetch_sales_history(months=3):
    uid, models = get_client()
    today = datetime.today()
    past = today.replace(day=1)
    past = past.replace(month=past.month - months if past.month > months else 1)
    domain = [[['date_order', '>=', past.strftime('%Y-%m-%d')]]]
    fields = ['date_order', 'amount_total']
    return models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'sale.order', 'search_read',
                             domain, {'fields': fields})
