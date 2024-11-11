{
    'name': 'AI Task Integration',
    'version': '1.0',
    'summary': 'Integrates AI API for task details in Odoo 17',
    'category': 'Project',
    'author': 'Your Name',
    'depends': ['project'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_task_view.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
