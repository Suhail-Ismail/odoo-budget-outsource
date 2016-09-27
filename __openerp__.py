# -*- coding: utf-8 -*-
{
    'name': "outsource",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,
    'application': True,
    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'tbpc',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'mail',
                ],

    # always loaded
    'data': [
        'data/outsource.contractor.csv',
        'data/outsource.unit.rate.csv',

        'views/purchase_order.xml',
        'views/purchase_order_collection.xml',
        'views/approval.xml',
        'views/contractor.xml',
        'views/unit_rate.xml',
        'views/resource.xml',
        'views/invoice.xml',

        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/approval.xml',
    ],
}