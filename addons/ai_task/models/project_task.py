import json
import re
import requests
import time
from odoo import api, fields, models

class ProjectTask(models.Model):
    _inherit = 'project.task'

    def markdown_to_html(self, markdown_text):
        """Convert a subset of Markdown to HTML with improved parsing for lists and headers."""
        # Convert headers (e.g., # Header, ## Header, ### Header)
        markdown_text = re.sub(r'(^|\n)#{1}\s+(.+)', r'\1<h1>\2</h1>', markdown_text)
        markdown_text = re.sub(r'(^|\n)#{2}\s+(.+)', r'\1<h2>\2</h2>', markdown_text)
        markdown_text = re.sub(r'(^|\n)#{3}\s+(.+)', r'\1<h3>\2</h3>', markdown_text)

        # Convert bold (e.g., **text** or __text__)
        markdown_text = re.sub(r'\*\*(.*?)\*\*|__(.*?)__', r'<strong>\1\2</strong>', markdown_text)

        # Convert italic (e.g., *text* or _text_)
        markdown_text = re.sub(r'\*(.*?)\*|_(.*?)_', r'<em>\1\2</em>', markdown_text)

        # Convert unordered lists (e.g., - item or * item)
        markdown_text = re.sub(r'(^|\n)[*-]\s+(.+)', r'\1<li>\2</li>', markdown_text)
        markdown_text = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', markdown_text, flags=re.DOTALL)

        # Convert ordered lists (e.g., multiple lines with "1. item")
        markdown_text = re.sub(r'(^|\n)1\.\s+(.+)', r'\1<li>\2</li>', markdown_text)
        markdown_text = re.sub(r'(<li>.*?</li>)', r'<ol>\1</ol>', markdown_text, flags=re.DOTALL)

        # Convert newlines to <br> tags (optional, if you want line breaks)
        markdown_text = markdown_text.replace('\n', '<br>')

        return markdown_text

    def action_send_to_ai(self):
        for task in self:
            query_data = {
                "task_name": task.name,
                "task_description": task.description,
                "task_deadline": task.date_deadline.isoformat() if task.date_deadline else None,
                "project_name": task.project_id.name,
            }
            request_data = {
                "inputs": {},
                "query": json.dumps(query_data),
                "response_mode": "blocking",
                "conversation_id": "",
                "user": self.env.user.login,
            }

            headers = {
                'Authorization': 'Bearer app-MxpJL6WwXRaZAD4PMenwVhnX',  # 替換為實際的 API key
                'Content-Type': 'application/json',
            }
            
            response = requests.post(
                'https://neobase.app/v1/chat-messages',
                headers=headers,
                json=request_data
            )
            
            if response.status_code == 200:
                response_data = response.json()
                answer = response_data.get('answer', 'No answer provided')
                conversation_id = response_data.get('conversation_id')

                try:
                    sub_tasks_data = json.loads(json.dumps(eval(answer)))
                    should_create_sub_task = len(sub_tasks_data) > 1
                except (json.JSONDecodeError, SyntaxError) as e:
                    sub_tasks_data = []
                    should_create_sub_task = False

                if conversation_id:
                    second_request_data = {
                        "inputs": {},
                        "query": "go",
                        "response_mode": "blocking",
                        "conversation_id": conversation_id,
                        "user": self.env.user.login,
                    }

                    second_response = requests.post(
                        'https://neobase.app/v1/chat-messages',
                        headers=headers,
                        json=second_request_data
                    )

                    if second_response.status_code == 200:
                        second_response_data = second_response.json()
                        second_answer = second_response_data.get('answer', 'No answer provided')

                        if should_create_sub_task:
                            sub_task_descriptions = second_answer.split('---')
                            for index, desc in enumerate(sub_task_descriptions, start=1):
                                sub_task_name = f"Sub Task {index}"
                                self.env['project.task'].create({
                                    'name': sub_task_name,
                                    'description': self.markdown_to_html(desc),
                                    'project_id': task.project_id.id,
                                    'parent_id': task.id,
                                })
                            task.message_post(body="已根據 AI 的回應建立子任務。")
                        else:
                            # 將 Markdown 內容轉換為 HTML
                            html_description = self.markdown_to_html(second_answer)
                            task.description = html_description
                            task.message_post(body="已根據 AI 的回應更新任務描述。")
                    else:
                        task.message_post(body="第二次請求失敗，狀態碼：" + str(second_response.status_code))
            else:
                task.message_post(body="第一次請求失敗，狀態碼：" + str(response.status_code))
