# my_module/controllers/main.py
from odoo import http
from odoo.http import request, Response
import json
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)

class TestController(http.Controller):
    
    @http.route('/api/test', type='http', auth='public', csrf=False)
    def test_endpoint(self):
        return "Hello, Controller is working!"
        
    @http.route('/api/test/json', type='json', auth='public', csrf=False)
    def test_json(self):
        return {
            "status": "success",
            "message": "JSON controller is working!"
        }
    
    @http.route('/api/test/info', type='http', auth='public', csrf=False)
    def test_info(self):
        return Response(
            json.dumps({
                'odoo_user': request.env.user.name,
                'url': request.httprequest.url,
                'method': request.httprequest.method,
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }),
            content_type='application/json'
        )
    
    @http.route('/api/prompts', type='http', auth='public', csrf=False)
    def get_prompts(self, **kwargs):
        try:
            domain = [('active', '=', True)]
            
            # 搜尋條件
            if kwargs.get('name'):
                domain.append(('name', 'ilike', kwargs['name']))
            if kwargs.get('tag_id'):
                domain.append(('tag_ids', 'in', [int(kwargs['tag_id'])]))
                
            # 分頁
            limit = int(kwargs.get('limit', 10))
            offset = int(kwargs.get('offset', 0))
            
            # 獲取資料
            prompts = request.env['prompt.prompt'].sudo().search_read(
                domain,
                ['name', 'content', 'description', 'usage_amount'],
                limit=limit,
                offset=offset,
                order='create_date desc'
            )
            
            return Response(
                json.dumps(prompts),
                content_type='application/json'
            )
        except Exception as e:
            return Response(
                json.dumps({'error': str(e)}),
                content_type='application/json',
                status=500
            )