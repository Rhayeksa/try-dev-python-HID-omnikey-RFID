# -*- coding: utf-8 -*-
import json
from datetime import datetime
from http import HTTPStatus

from odoo.http import request

from odoo import http


class RestApi(http.Controller):
    now = datetime.now()

    @http.route('/rest_api/rest_api', auth='public')
    def index(self, **kw):
        return "Hello, world. Rhayeksa"

    @http.route('/rest_api/rest_api/objects', auth='public')
    def list(self, **kw):
        return http.request.render('rest_api.listing', {
            'root': '/rest_api/rest_api',
            'objects': http.request.env['rest_api.rest_api'].search([]),
        })

    @http.route('/rest_api/rest_api/objects/<model("rest_api.rest_api"):obj>', auth='public')
    def object(self, obj, **kw):
        return http.request.render('rest_api.object', {
            'object': obj
        })

    @http.route('/api/customers', type='http', auth='user', methods=['GET'], csrf=False)
    def get_customers(self, **kwargs):
        # customers = request.env['res.partner'].sudo().search(
        #     [('customer_rank', '>', 0)])
        customers = request.env['res.partner']
        data = [{
            'id': c.id,
            'name': c.name,
            'email': c.email,
        } for c in customers]
        return http.Response(
            json.dumps(data),
            content_type='application/json',
            status=200
        )

    # @http.route('/api/read-rfid', type='http', auth='user', methods=['POST'], csrf=False)
    # @http.route('/api/read-rfid', type='http', auth='public', methods=['GET'], csrf=False)
    @http.route('/api/read-rfid', type='http', auth='public', methods=['POST'], csrf=False)
    def get_customers(self, **kwargs):
        data = json.loads(request.httprequest.data)

        code = 200
        code = HTTPStatus(code)
        status = code.phrase
        msg = None
        req = data.get("rfid")

        result = {
            "datetime": self.now.isoformat(),
            "code": code,
            "status": status,
            "msg": msg if msg != None else status,
            "data": req,
        }
        return http.Response(
            json.dumps(result),
            content_type='application/json',
            status=code
        )
        # return result
