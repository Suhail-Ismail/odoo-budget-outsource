# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Resource(models.Model):
    _name = 'outsource.resource'
    _rec_name = 'full_name'
    _description = 'Resource'

    # BASIC FIELDS
    # ----------------------------------------------------------
    type = fields.Char(string='Type')
    type_class = fields.Char(string='Type Class')
    agency_ref_num = fields.Char(string='Agency Reference')
    emp_num = fields.Char(string='Employee Number')
    full_name = fields.Char(string='Full Name')
    date_of_join = fields.Date(string='Date of Join')
    job_title = fields.Char(string='Job Title')
    grade_level = fields.Char(string='Grade Level')
    po_position = fields.Char(string='PO Position')
    po_level = fields.Char(string='PO Level')
    division = fields.Char(string='Division')
    section = fields.Char(string='Section')
    manager = fields.Char(string='Manager')
    rate = fields.Float(string='Rate', digits=(32, 2), default=0.00)
    po_rate_percent_increase = fields.Float(string='% inc', digits=(32, 2), default=0.00)
    capex_percent = fields.Float(string='% CAPEX', digits=(32, 2), default=0.00)
    capex_rate = fields.Float(string='CAPEX rate', digits=(32, 2), default=0.00)
    opex_percent = fields.Float(string='% OPEX', digits=(32, 2), default=0.00)
    opex_rate = fields.Float(string='OPEX rate', digits=(32, 2), default=0.00)
    revenue_percent = fields.Float(string='% Revenue', digits=(32, 2), default=0.00)
    revenue_rate = fields.Float(string='Revenue Rate', digits=(32, 2), default=0.00)
    remarks = fields.Text()
    capex_commitment_value = fields.Float(string='CAPEX Commitment', digits=(32, 2), default=0.00)
    opex_value = fields.Float(string='OPEX Value', digits=(32, 2), default=0.00)
    revenue_value = fields.Float(string='Revenue Value', digits=(32, 2), default=0.00)
    job_id = fields.Char(string='job_id')
    has_tool_or_uniform = fields.Boolean(string='has tool or uniform')

    # RELATIONSHIPS
    # ----------------------------------------------------------
    po_line_detail_id = fields.Many2one('outsource.purchase.order.line.detail', string='Line Detail')
    contractor_id = fields.Many2one('res.partner', string='Contractor')
    invoice_ids = fields.One2many('outsource.invoice', 'resource_id', string="Resources")