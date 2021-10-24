# -*- coding: utf-8 -*-
# from odoo import http


# class Qrcode(http.Controller):
#     @http.route('/qrcode/qrcode/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/qrcode/qrcode/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('qrcode.listing', {
#             'root': '/qrcode/qrcode',
#             'objects': http.request.env['qrcode.qrcode'].search([]),
#         })

#     @http.route('/qrcode/qrcode/objects/<model("qrcode.qrcode"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('qrcode.object', {
#             'object': obj
#         })
