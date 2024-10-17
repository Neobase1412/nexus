# -*- coding: utf-8 -*-
{
    'name': "Real Estate",

    'summary': """
        Starting module for "Discover the JS framework, chapter 1: Owl components"
    """,

    'description': """
        Starting module for "Discover the JS framework, chapter 1: Owl components"
    """,

    'author': "PartnerAI",
    'website': "https://www.odoo.com",

    'category': 'Tutorials/Estate',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menus.xml',
    ],
    'application': True,
    'installable': True,
    'license': 'AGPL-3'
}