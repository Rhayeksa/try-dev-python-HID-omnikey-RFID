# -*- coding: utf-8 -*-
import json
from datetime import datetime
from http import HTTPStatus

from odoo.http import request

from odoo import http


class TreeDetection(http.Controller):
    _now = datetime.now()

    # util
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

    def _upsert(self, rfid: str):
        try:
            request.env.cr.execute(
                """
                SELECT counter_check, planting_date FROM tree_model WHERE rfid_tag = %s
                """, (rfid,)
            )
            data = self._fetchone_dict(request.env.cr)
            if not data:
                request.env.cr.execute(
                    """
                    INSERT INTO tree_model(rfid_tag, create_date)
                    VALUES(%s, %s)
                    """, (
                        rfid,
                        self._now,
                    )
                )
                return self._response(code=201, msg=f"Inisiasi RFID {rfid}")

            request.env.cr.execute(
                """
                UPDATE tree_model 
                SET datetime_check = %s
                    , counter_check = %s
                    , age = %s
                WHERE rfid_tag = %s
                """, (
                    self._now if data["planting_date"] else None,
                    data["counter_check"]+1 if data["counter_check"] else None,
                    (
                        self._now.date() - data["planting_date"]
                    ).days if data["planting_date"] else None,
                    rfid,
                )
            )
            return self._response(code=200, msg=f"Tree {rfid} updated")
        except Exception as e:
            return self._response(code=500, msg=str(e))
    # end util

    # html page
    @http.route('/tree-detection', type='http', auth='public', methods=['GET'], csrf=False)
    def _tree_detection(self, **kw):
        return """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Odoo RFID</title>
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css"
      rel="stylesheet"
    />
    <script src="https://unpkg.com/htmx.org@1.9.2"></script>
  </head>
  <body>
    <div class="container mt-3">
      <div class="card text-center mb-3">
        <div class="card-header h5">RFID Code</div>
        <div class="card-body">
          <form
            id="rfid-form"
            hx-post="/api/tree-detection/form-html"
            hx-target="#alert-box"
            hx-swap="none"
            method="post"
          >
            <div class="input-group">
              <span class="input-group-text fw-bold" id="visible-addon">| | | | |</span>
              <input
                name="id_tag"
                autofocus
                type="text"
                class="form-control"
                placeholder="RFID Code"
                aria-label="RFID"
                aria-describedby="visible-addon"
              />
            </div>
            <button type="submit" class="btn btn-primary mt-3" hidden>Submit</button>
          </form>
        </div>
        <div class="card-footer text-body-secondary">(^_^)</div>
      </div>

      <!-- Alert target -->
      <div id="alert-box"></div>
    </div>

    <script>
      document.body.addEventListener('htmx:afterRequest', function (event) {
        const xhr = event.detail.xhr;
        const alertBox = document.getElementById('alert-box');

        try {
          const res = JSON.parse(xhr.responseText);
          const msg = res.msg || 'Tidak ada pesan.';
          const code = res.code;

          const alertClass =
            code === 200
              ? 'alert alert-success'
              : 'alert alert-success';

          alertBox.innerHTML = `<div class="${alertClass} mt-3" role="alert">${msg}</div>`;
        } catch (e) {
          alertBox.innerHTML =
            '<div class="alert alert-danger mt-3" role="alert">❌ Gagal memproses respons dari server.</div>';
        }
      });
    </script>
  </body>
</html>"""
    # end html page


    # api
    @http.route('/api/tree-detection/json-req', type='http', auth='public', methods=['POST'], csrf=False)
    def _upsert_with_json(self, **kw):
        req = json.loads(request.httprequest.data)
        return self._upsert(rfid=req.get("id_tag"))

    @http.route('/api/tree-detection/form-html', type='http', auth='public', methods=['POST'], csrf=False)
    def _upsert_with_form(self, **kw):
        return self._upsert(rfid=kw.get("id_tag"))
    # end api

