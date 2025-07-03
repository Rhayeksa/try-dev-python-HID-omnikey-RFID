from odoo import http
from odoo.http import request
import json

class ProductApiController(http.Controller):

    @http.route('/api/products', type='http', auth='public', methods=['GET'], csrf=False)
    def get_products(self, **kwargs):
        try:
            request.env.cr.execute("SELECT id, name FROM product_product LIMIT 10")
            rows = request.env.cr.fetchall()
            result = [{'id': row[0], 'name': row[1]} for row in rows]
            return http.Response(json.dumps(result), content_type='application/json', status=200)
        except Exception as e:
            return http.Response(json.dumps({'error': str(e)}), content_type='application/json', status=500)

    @http.route('/api/products', type='http', auth='public', methods=['POST'], csrf=False)
    def create_product(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
            name = data.get('name')
            if not name:
                return http.Response(json.dumps({'error': 'Missing name'}), status=400, content_type='application/json')
            
            query = "INSERT INTO product_product (name, create_uid, create_date, write_uid, write_date) VALUES (%s, %s, now(), %s, now()) RETURNING id"
            user_id = request.env.user.id
            request.env.cr.execute(query, (name, user_id, user_id))
            product_id = request.env.cr.fetchone()[0]
            return http.Response(json.dumps({'id': product_id, 'name': name}), content_type='application/json', status=201)
        except Exception as e:
            return http.Response(json.dumps({'error': str(e)}), content_type='application/json', status=500)

    @http.route('/api/products/<int:product_id>', type='http', auth='public', methods=['PUT'], csrf=False)
    def update_product(self, product_id, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
            name = data.get('name')
            if not name:
                return http.Response(json.dumps({'error': 'Missing name'}), status=400, content_type='application/json')

            request.env.cr.execute("SELECT id FROM product_product WHERE id = %s", (product_id,))
            if not request.env.cr.fetchone():
                return http.Response(json.dumps({'error': 'Product not found'}), content_type='application/json', status=404)

            request.env.cr.execute("UPDATE product_product SET name = %s, write_uid = %s, write_date = now() WHERE id = %s", (name, request.env.user.id, product_id))
            return http.Response(json.dumps({'message': 'Product updated'}), content_type='application/json', status=200)
        except Exception as e:
            return http.Response(json.dumps({'error': str(e)}), content_type='application/json', status=500)

    @http.route('/api/products/<int:product_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_product(self, product_id, **kwargs):
        try:
            request.env.cr.execute("SELECT id FROM product_product WHERE id = %s", (product_id,))
            if not request.env.cr.fetchone():
                return http.Response(json.dumps({'error': 'Product not found'}), content_type='application/json', status=404)

            request.env.cr.execute("DELETE FROM product_product WHERE id = %s", (product_id,))
            return http.Response(json.dumps({'message': 'Product deleted'}), content_type='application/json', status=200)
        except Exception as e:
            return http.Response(json.dumps({'error': str(e)}), content_type='application/json', status=500)
