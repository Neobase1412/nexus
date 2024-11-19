{
    'name': 'Prompt Library',
    'version': '17.0.1.0.0',
    'category': 'Productivity',
    'summary': 'Manage AI prompts',
    'description': """Prompt Library for managing AI prompts""",
    'depends': ['base', 'mail'],  # Added mail dependency
    'data': [
        'security/ir.model.access.csv',
        'views/prompt_views.xml',
    ],
    'controllers': ['controllers/controllers.py'],
    'application': True,
    'installable': True,
    'licence': 'LGPL-3',
}