# models/models.py
from odoo import models, fields, api
from datetime import datetime

class Prompt(models.Model):
    _name = 'prompt.prompt'
    _description = 'Prompt Library'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'  # 按創建日期排序，最新的在前面

    name = fields.Text(
        string='Prompt Name', 
        required=True, 
        tracking=True,
        help="Enter the name or title of your prompt"
    )
    active = fields.Boolean(
        string='Active', 
        default=True, 
        tracking=True,
        help="If unchecked, it will be archived"
    )
    content = fields.Text(
        string='Prompt Content',
        tracking=True,
        help="The main content of your prompt"
    )
    description = fields.Text(
        string='Description',
        tracking=True,
        help="Additional description or notes about the prompt"
    )
    usage_amount = fields.Integer(
        string='Usage Count', 
        default=0, 
        tracking=True,
        help="Number of times this prompt has been used"
    )
    tag_ids = fields.Many2many(
        'prompt.tag', 
        string='Tags', 
        tracking=True,
        help="Categorize your prompts with tags"
    )
    
    # 系統欄位
    create_date = fields.Datetime(
        string='Created At', 
        readonly=True, 
        default=lambda self: fields.Datetime.now()
    )
    create_uid = fields.Many2one(
        'res.users', 
        string='Created By', 
        readonly=True, 
        default=lambda self: self.env.user
    )
    write_date = fields.Datetime(
        string='Updated At', 
        readonly=True
    )
    write_uid = fields.Many2one(
        'res.users', 
        string='Updated By', 
        readonly=True
    )

    # 增加使用次數的方法
    def increment_usage(self):
        for record in self:
            record.usage_amount += 1

    def write(self, vals):
        vals.update({
            'write_date': fields.Datetime.now(),
            'write_uid': self.env.user.id,
        })
        return super(Prompt, self).write(vals)

class PromptTag(models.Model):
    _name = 'prompt.tag'
    _description = 'Prompt Tag'
    _inherit = ['mail.thread']
    _order = 'name asc'  # 按名稱字母順序排序

    name = fields.Char(
        string='Tag Name', 
        required=True, 
        tracking=True,
        help="Name of the tag"
    )
    color = fields.Integer(
        string='Color Index',
        help="Choose a color for the tag"
    )
    prompt_count = fields.Integer(
        string='Prompt Count',
        compute='_compute_prompt_count',
        help="Number of prompts using this tag"
    )
    
    # 系統欄位
    create_date = fields.Datetime(
        string='Created At', 
        readonly=True, 
        default=lambda self: fields.Datetime.now()
    )
    create_uid = fields.Many2one(
        'res.users', 
        string='Created By', 
        readonly=True, 
        default=lambda self: self.env.user
    )
    write_date = fields.Datetime(
        string='Updated At', 
        readonly=True
    )
    write_uid = fields.Many2one(
        'res.users', 
        string='Updated By', 
        readonly=True
    )

    @api.depends('name')
    def _compute_prompt_count(self):
        for tag in self:
            tag.prompt_count = self.env['prompt.prompt'].search_count([('tag_ids', 'in', tag.id)])

    def write(self, vals):
        vals.update({
            'write_date': fields.Datetime.now(),
            'write_uid': self.env.user.id,
        })
        return super(PromptTag, self).write(vals)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists!"),
    ]