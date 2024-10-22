# -*- coding: utf-8 -*-
{
    'name': "AI Enhanced",

    'summary': """
        AI Enhanced
    """,

    'description': """
        AI Enhanced
    """,

    'author': "PartnerAI",
    'website': "https://www.odoo.com",

    'category': 'Tutorials/Estate',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'estate'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_ai_views.xml',
    ],
    'application': True,
    'installable': True,
    'license': 'AGPL-3'
}