# -*- coding: utf-8 -*-

from odoo import models, fields


class UnitRate(models.Model):
    _name = 'outsource.unit.rate'
    _rec_name = 'po_position'
    _description = 'Unit Rate'
    _inherit = ['outsource.accessdb.mixin']

    contractor = fields.Char()
    po_position = fields.Char()
    po_level = fields.Char()
    amount = fields.Float(default=0.00)
    percent = fields.Integer(default=0)
