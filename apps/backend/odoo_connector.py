import xmlrpc.client
from datetime import datetime, timedelta

class OdooConnector:
    def __init__(self, url, db, username, password):
        common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
        self.uid = common.authenticate(db, username, password, {})
        self.models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
        self.db = db
        self.pw = password

    def fetch_monthly_sales(self):
        """Return total and list of sales orders from 1st of month to today."""
        today = datetime.today()
        first = today.replace(day=1).strftime("%Y-%m-%d")
        sales = self.models.execute_kw(
            self.db, self.uid, self.pw,
            'sale.order', 'search_read',
            [[['date_order', '>=', first]]],
            {'fields': ['name', 'amount_total'], 'limit': 1000}
        )
        total = sum(float(s['amount_total']) for s in sales)
        return total, sales
