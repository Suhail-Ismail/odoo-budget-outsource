# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Resource(models.Model):
    _name = 'outsource.resource'
    _rec_name = 'res_full_name'
    _description = 'Resource'
    _inherit = ['outsource.accessdb.mixin']

    res_type = fields.Char()
    res_type_class = fields.Char()
    agency_ref_num = fields.Char()
    res_emp_num = fields.Char()
    res_full_name = fields.Char()
    date_of_join = fields.Date()
    res_job_title = fields.Char()
    grade_level = fields.Char()
    po_position = fields.Char()
    po_level = fields.Char()
    division = fields.Char()
    section = fields.Char()
    manager = fields.Char()
    director = fields.Char()
    rate = fields.Float(default=0.00)
    po_rate_percent_increase = fields.Float(default=0.00)
    capex_percent = fields.Integer(default=0)
    capex_rate = fields.Float(default=0.00)
    opex_percent = fields.Integer(default=0)
    opex_rate = fields.Float(default=0.00)
    revenue_percent = fields.Integer(default=0)
    revenue_rate = fields.Float(default=0.00)
    remarks = fields.Text()
    po_num = fields.Char()
    po_value = fields.Float(default=0.00)
    capex_commitment_value = fields.Float(default=0.00)
    opex_value = fields.Float(default=0.00)
    revenue_value = fields.Float(default=0.00)
    contractor = fields.Char()
    po_os_ref = fields.Char()
    has_tool_or_uniform = fields.Boolean()

    # RELATIONSHIPS
    # ----------------------------------------------------------
    po_line_detail_id = fields.Many2one('outsource.purchase.order.line.detail', string='Line Detail')
    po_id = fields.Many2one('outsource.purchase.order', string='Purchase Order')
