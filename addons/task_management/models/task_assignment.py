# models/task_assignment.py
from odoo import models, fields, api

class TaskAssignment(models.Model):
    _name = 'task.assignment'
    _description = 'Task Assignment'

    form_responsible_id = fields.Many2one(
        'res.users', string='Form Responsible', default=lambda self: self.env.user, required=True)
    task_type = fields.Selection([
        ('development', 'Development'),
        ('testing', 'Testing'),
        ('deployment', 'Deployment'),
        ('research', 'Research'),
        ('maintenance', 'Maintenance'),
    ], string='Task Type', required=True)
    task_responsible_id = fields.Many2one(
        'res.users', string='Task Responsible', required=True)
    task_executor_ids = fields.Many2many(
        'res.users', string='Task Executors', required=True)
    project_id = fields.Many2one(
        'project.project', string='Project', required=False)
    expected_delivery_date = fields.Date(
        string='Expected Delivery Date', required=True)
    note = fields.Text(string='Note')
