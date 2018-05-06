# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Resource(models.Model):
    _name = 'budget.outsource.resource'
    _rec_name = 'name'
    _description = 'Resource'
    _inherit = ['mail.thread', 'budget.enduser.mixin']

    name = fields.Char()
    type = fields.Char()
    type_class = fields.Char()
    agency_ref_num = fields.Char()
    emp_num = fields.Char()
    date_of_join = fields.Date()
    has_tool_or_uniform = fields.Boolean()

    capex_percent = fields.Integer(default=0)
    opex_percent = fields.Integer(default=0)
    revenue_percent = fields.Integer(default=0)

    # RELATIONSHIPS
    # ----------------------------------------------------------
    contractor_id = fields.Many2one('budget.contractor.contractor', string='Contractor')
