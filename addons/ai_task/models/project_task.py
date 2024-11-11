import json
import re
import requests
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

                # 處理 answer 作為字串形式的 JSON 陣列
                try:
                    parsed_sub_tasks = json.loads(json.dumps(eval(answer)))
                    should_create_sub_task = len(parsed_sub_tasks) > 1
                except (json.JSONDecodeError, SyntaxError) as e:
                    parsed_sub_tasks = []
                    should_create_sub_task = False
                    task.message_post(body=f"解析 AI 回應失敗：{e}")
                
                # 根據 parsed_sub_tasks 建立子任務或更新描述
                if should_create_sub_task:
                    for sub_task in parsed_sub_tasks:
                        title = sub_task.get('title', 'Untitled Task')
                        document = sub_task.get('document', 'No description provided')

                        self.env['project.task'].create({
                            'name': title,
                            'description': self.markdown_to_html(document),
                            'project_id': task.project_id.id,
                            'parent_id': task.id,
                        })
                    task.message_post(body="已根據 AI 的回應建立子任務。")
                else:
                    # 將單一任務描述轉換為 HTML
                    html_description = self.markdown_to_html(answer)
                    task.description = html_description
                    task.message_post(body="已根據 AI 的回應更新任務描述。")
            else:
                task.message_post(body="請求失敗，狀態碼：" + str(response.status_code))
