# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Resource(models.Model):
    _name = 'budget.outsource.resource'
    _rec_name = 'name'
    _description = 'Resource'
    _inherit = ['mail.thread', 'budget.enduser.mixin']

    type = fields.Char()
    type_class = fields.Char()
    agency_ref_num = fields.Char()
    emp_num = fields.Char()
    name = fields.Char()
    date_of_join = fields.Date()
    has_tool_or_uniform = fields.Boolean()

    # rate = fields.Float(default=0.00)
    # capex_percent = fields.Integer(default=0)
    # capex_rate = fields.Float(default=0.00)
    # opex_percent = fields.Integer(default=0)
    # opex_rate = fields.Float(default=0.00)
    # revenue_percent = fields.Integer(default=0)
    # revenue_rate = fields.Float(default=0.00)
    # remarks = fields.Text()
    # po_num = fields.Char()
    # po_value = fields.Float(default=0.00)
    # capex_commitment_value = fields.Float(default=0.00)
    # opex_value = fields.Float(default=0.00)
    # revenue_value = fields.Float(default=0.00)
    # contractor = fields.Char()
    # po_os_ref = fields.Char()
    #
    # po_rate_percent_increase = fields.Float(default=0.00)

    # RELATIONSHIPS
    # ----------------------------------------------------------
    # po_line_detail_id = fields.Many2one('outsource.purchase.order.line.detail', string='Line Detail')
    # po_id = fields.Many2one('outsource.purchase.order', string='Purchase Order')
