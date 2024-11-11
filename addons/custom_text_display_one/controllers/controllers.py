# -*- coding: utf-8 -*-
from odoo import http


class CustomTextDisplayOne(http.Controller):
    @http.route('/custom_text_display_one/custom_text_display_one', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/custom_text_display_one/custom_text_display_one/objects', auth='public')
    def list(self, **kw):
        return http.request.render('custom_text_display_one.listing', {
            'root': '/custom_text_display_one/custom_text_display_one',
            'objects': http.request.env['custom_text_display_one.custom_text_display_one'].search([]),
        })

    @http.route('/custom_text_display_one/custom_text_display_one/objects/<model("custom_text_display_one.custom_text_display_one"):obj>', auth='public')
    def object(self, obj, **kw):
        return http.request.render('custom_text_display_one.object', {
            'object': obj
        })

