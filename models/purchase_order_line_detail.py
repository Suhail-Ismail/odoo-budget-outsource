# -*- coding: utf-8 -*-
from odoo import models, fields, api

class PurchaseOrderLineDetail(models.Model):
    _name = 'outsource.purchase.order.line.detail'
    _rec_name = 'po_os_ref'
    _description = 'Purchase Order Line Detail'
    _inherit = ['outsource.accessdb.mixin']

    # BASIC FIELDS
    # ----------------------------------------------------------
    
    po_os_ref = fields.Char()
    po_position = fields.Char()
    po_level = fields.Char()
    po_rate = fields.Float(default=0.00)
    po_revise_rate = fields.Float(default=0.00)
    division = fields.Char()
    section = fields.Char()
    sub_section = fields.Char()
    director_name = fields.Char()
    frozen_status = fields.Char()
    approval_ref_num = fields.Char()
    approval_reason = fields.Text(blank=True)
    kpi_2016 = fields.Char()
    capex_percent = fields.Integer(default=0)
    opex_percent = fields.Integer(default=0)
    revenue_percent = fields.Integer(default=0)
    rate_diff_percent = fields.Float(default=0.00)

    # RELATIONSHIPS
    # ----------------------------------------------------------
    po_line_id = fields.Many2one('outsource.purchase.order.line', string='Purchase Order Line')

    # TODO BELOW IS DJANGO CODE, CHECK IF IT ALSO NEEDED FOR ODOO
    # @property
    # def rate(self):
    #     return self.po_revise_rate if self.po_revise_rate != Decimal('0.00') else self.po_rate
    #
