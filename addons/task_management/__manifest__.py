# __manifest__.py
{
    'name': 'Task Management',
    'version': '1.0',
    'summary': 'Module for managing tasks assigned by PM to the engineering team.',
    'description': 'This module allows PMs to assign tasks to engineers, track progress, and manage related information.',
    'author': 'Your Name',
    'website': 'https://yourwebsite.com',
    'category': 'Project',
    'depends': ['base', 'project'],
    'data': [
        'security/task_assignment_security.xml',
        'security/ir.model.access.csv',
        'views/task_assignment_views.xml',
        'views/task_assignment_menus.xml',
        'data/task_assignment_data.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
