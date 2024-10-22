
from odoo import api, fields, models
import requests

class EstatePropertyAI(models.Model):
    _inherit = 'estate.property'

    ai_generated_description = fields.Text(string="AI Generated Description")

    def action_generate_ai_description(self):
        # Example of calling an external AI server API to generate property description
        url = "https://neobase.app/v1/chat-messages"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer app-MxpJL6WwXRaZAD4PMenwVhnX',
        }
        payload = {
            "inputs": {},
            "query": '測試',
            "response_mode": 'blocking',
            "conversation_id": '',
            "user": 'odoo',
            "files": [],
        }
        response = requests.post(url, json=payload, headers=headers)
        print(response.json())
        if response.status_code == 200:
            self.ai_generated_description = response.json().get("answer")
        else:
            raise ValueError("Failed to get response from AI server")
