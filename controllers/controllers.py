# -*- coding: utf-8 -*-
from openerp import http

# class Resource(http.Controller):
#     @http.route('/resource/resource/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/resource/resource/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('resource.listing', {
#             'root': '/resource/resource',
#             'objects': http.request.env['resource.resource'].search([]),
#         })

#     @http.route('/resource/resource/objects/<model("resource.resource"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('resource.object', {
#             'object': obj
#         })