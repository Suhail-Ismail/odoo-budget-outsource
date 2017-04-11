# -*- coding: utf-8 -*-
{
    'name': "Outsource",
    'version': '0.1',
    'summary': 'Outsource Management',
    'sequence': 9,
    'description': """
Odoo Module
===========
Specifically Designed for Etisalat-TBPC

Outsource Management
---------------------
- Approval
- Claim
- Contractor
- Contractor Contact
- Purchase Order
- Resource
- Unit Rate
    """,
    'author': "Marc Philippe de Villeres",
    'website': "https://github.com/mpdevilleres",
    'category': 'TBPC Budget',
    'depends': ['base', 'document'],
    'data': [
        'security/budget_outsource.xml',
        'security/ir.model.access.csv',

        'views/invoice.xml',
        'views/resource.xml',
        'views/unit_rate.xml',
        'views/purchase_order.xml',
        'views/purchase_order_line.xml',
        'views/purchase_order_line_detail.xml',

        'views/summary_sheet.xml',

        'views/menu.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
