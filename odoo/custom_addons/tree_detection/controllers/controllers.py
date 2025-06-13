# -*- coding: utf-8 -*-
# from odoo import http


# class TreeDetection(http.Controller):
#     @http.route('/tree_detection/tree_detection', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tree_detection/tree_detection/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tree_detection.listing', {
#             'root': '/tree_detection/tree_detection',
#             'objects': http.request.env['tree_detection.tree_detection'].search([]),
#         })

#     @http.route('/tree_detection/tree_detection/objects/<model("tree_detection.tree_detection"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tree_detection.object', {
#             'object': obj
#         })

