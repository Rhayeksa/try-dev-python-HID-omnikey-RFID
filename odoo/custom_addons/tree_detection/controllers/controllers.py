# -*- coding: utf-8 -*-
import json
from datetime import datetime
from http import HTTPStatus

from odoo.http import request

from odoo import http


class TreeDetection(http.Controller):
    _now = datetime.now()

    def _response(self, code: int, msg: str = None, page: dict = None, data=None):
        status = None
        try:
            code = HTTPStatus(code)
            status = code.phrase
        except Exception as e:
            print(f"\nError: {e}\n")
            msg = str(e)
            data = None

        result = {
            "datetime": str(self._now.isoformat()),
            "code": code,
            "status": status,
            "msg": msg if msg != None else status,
        }
        result.update({"page": page} if page != None else {})
        result.update({"data": data})
        return http.Response(
            json.dumps(result),
            content_type='application/json',
            status=code
        )

    def _fetchall_dict(self, cr):
        """Ambil semua hasil query sebagai list of dict"""
        columns = [col.name for col in cr.description]
        return [dict(zip(columns, row)) for row in cr.fetchall()]

    def _fetchone_dict(self, cr):
        """Ambil satu hasil query sebagai dict"""
        columns = [col.name for col in cr.description]
        row = cr.fetchone()
        return dict(zip(columns, row)) if row else None

    @http.route('/api/tree-detection/<string:rfid>', type='http', auth='public', methods=['PUT'], csrf=False)
    def _update_tree(self, rfid, **kw):
        try:
            # req = json.loads(request.httprequest.data)
            # req = {
            #     "name": req.get("name")
            # }

            request.env.cr.execute(
                """
                SELECT counter_check, planting_date FROM tree_model WHERE rfid_tag = %s
                """, (rfid,)
            )
            data = self._fetchone_dict(request.env.cr)
            if not data:
                return self._response(code=404, msg=f"RFID {rfid} tidak terdaftar")

            request.env.cr.execute(
                """
                UPDATE tree_model 
                SET datetime_check = %s
                    , counter_check = %s
                    , age = %s
                WHERE rfid_tag = %s
                """, (
                    self._now,
                    data["counter_check"]+1,
                    (self._now.date() - data["planting_date"]).days,
                    rfid,
                )
            )
            return self._response(code=200, msg=f"Tree {rfid} updated")
        except Exception as e:
            return self._response(code=500, msg=str(e))
