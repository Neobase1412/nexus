from odoo import models, fields, api

class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.model
    def create(self, vals):
        # 調用父類的 create 方法
        project = super(ProjectProject, self).create(vals)

        # 定義默認的 stages，調整順序
        default_stages = [
            {'name': 'Pending', 'sequence': 1, 'project_ids': [(4, project.id)]},
            {'name': 'Not Started', 'sequence': 2, 'project_ids': [(4, project.id)]},
            {'name': 'Processing', 'sequence': 3, 'project_ids': [(4, project.id)]},
            {'name': 'Done', 'sequence': 4, 'project_ids': [(4, project.id)]},
        ]

        # 為該 Project 添加 stages
        for stage_vals in default_stages:
            self.env['project.task.type'].create(stage_vals)

        return project
