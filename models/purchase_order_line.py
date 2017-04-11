# -*- coding: utf-8 -*-
from odoo import models, fields, api

class PurchaseOrderLine(models.Model):
    _name = 'outsource.purchase.order.line'
    _description = 'Purchase Order Line'
    _rec_name = 'line_num'
    _inherit = ['outsource.accessdb.mixin']

    line_num = fields.Char(string='Line Number')
    line_duration = fields.Integer(string='Duration', default=0)
    line_value = fields.Float(default=0.00)
    line_revise_rate = fields.Float(default=0.00)
    line_rate = fields.Float(default=0.00)
    line_status = fields.Char(string='Status')
    line_actuals = fields.Float(default=0.00)
    capex_percent = fields.Float(default=0.00)
    opex_percent = fields.Float(default=0.00)
    revenue_percent = fields.Float(default=0.00)

    # RELATIONSHIPS
    # ----------------------------------------------------------
    po_id = fields.Many2one('outsource.purchase.order', string='Purchase Order')
    po_line_detail_ids = fields.One2many('outsource.purchase.order.line.detail',
                                  'po_line_id',
                                  string="Line Details")

    # TODO BELOW IS DJANGO CODE, CHECK IF IT ALSO NEEDED FOR ODOO
    # @property
    # def rate(self):
    #     return self.line_revise_rate if self.line_revise_rate != Decimal('0.00') else self.line_rate
