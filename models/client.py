#-*- coding: utf-8 -*-

from odoo import models, fields, api

class client(models.Model):
    _inherit = "res.partner"
    _description = "Les client qui achete la farine gmm"

    etiquette_id = fields.One2many("farinegmm.etiquette", "client_id", string="etiquettes")
