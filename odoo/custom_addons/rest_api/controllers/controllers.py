# -*- coding: utf-8 -*-
import json
from datetime import datetime
from http import HTTPStatus

from odoo.http import request

from odoo import http


class RestApi(http.Controller):
    now = datetime.now()

    # @http.route('/api/read-rfid', type='http', auth='user', methods=['POST'], csrf=False)
    # @http.route('/api/read-rfid', type='http', auth='public', methods=['GET'], csrf=False)
    @http.route('/api/read-rfid', type='http', auth='public', methods=['POST'], csrf=False)
    def get_rfid(self, **kwargs):
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
