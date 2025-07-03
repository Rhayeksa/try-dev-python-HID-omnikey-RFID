from odoo import http
from odoo.http import request
import json

class RawQueryApi(http.Controller):

    def _check_api_key(self):
        api_key = request.httprequest.headers.get('X-API-KEY')
        user = request.env['res.users'].sudo().search([('x_api_key', '=', api_key)], limit=1)
        if user:
            request.uid = user.id
            return True
        return False

    @http.route('/api/raw/products', type='http', auth='user', methods=['GET'], csrf=False)
    def get_products_raw(self, **kwargs):
        if not self._check_api_key():
            return http.Response(json.dumps({'error': 'Unauthorized'}), status=401, content_type='application/json')

        try:
            query = "SELECT id, name FROM product_product LIMIT 10"
            request.cr.execute(query)
            results = request.cr.fetchall()
            columns = [desc[0] for desc in request.cr.description]
            data = [dict(zip(columns, row)) for row in results]

            return http.Response(json.dumps(data), content_type='application/json', status=200)
        except Exception as e:
            return http.Response(json.dumps({'error': str(e)}), content_type='application/json', status=500)
