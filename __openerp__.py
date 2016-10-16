# -*- coding: utf-8 -*-
{
    'name': "Outsource",
    'version': '0.1',
    'summary': 'Outsource Management',
    'sequence': 4,
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
    'depends': ['budget_contractor'],
    'data': [
        'security/budget_outsource.xml',
        'security/ir.model.access.csv',
        'security/approval_security.xml',
        'security/purchase_order_security.xml',

        'views/purchase_order.xml',
        'views/purchase_order_collection.xml',
        'views/approval.xml',
        'views/contractor.xml',
        'views/unit_rate.xml',
        'views/resource.xml',
        'views/invoice.xml',

        'views/menu.xml',
    ],
    'demo': [
        'data/contractor.xml',
        'data/outsource.unit.rate.csv',
        'data/outsource.approval.csv',
        'data/outsource.required.team.csv',
        'data/outsource.purchase.order.csv',
        'data/outsource.purchase.order.line.csv',
        'data/outsource.purchase.order.line.detail.csv',
        'data/res.partner.csv'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
