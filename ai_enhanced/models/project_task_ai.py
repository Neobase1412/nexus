from odoo import api, fields, models
import requests

class ProjectTaskAI(models.Model):
    _inherit = 'project.task'

    def action_generate_ai_description(self):
        # Example of calling an external AI server API to generate task description
        print(self)
        name_value = self.name if self.name else ''
        payload = {
            "query": name_value,
            "inputs": {},
            "response_mode": 'blocking',
            "conversation_id": 'd2e7e12f-19ad-49fe-87cd-eb40e4813b93',
            "user": 'odoo',
            "files": [],
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer app-MxpJL6WwXRaZAD4PMenwVhnX',
        }
        url = "https://neobase.app/v1/chat-messages"

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            self.description = response.json().get("answer")
        else:
            raise ValueError("Failed to get response from AI server")
