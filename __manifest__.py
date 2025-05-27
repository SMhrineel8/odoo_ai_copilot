{
    'name': 'AI Copilot for Odoo',
    'version': '1.0.0',
    'summary': 'ChatGPT-powered Copilot for smarter ERP use',
    'description': 'Natural language chat, report generation, and forecasts from your Odoo data.',
    'author': 'Your Name or Brand',
    'category': 'Productivity',
    'website': 'https://yourdomain.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/copilot_view.xml',
    ],
    'installable': True,
    'application': True,
}
