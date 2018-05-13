# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Resource(models.Model):
    _name = 'budget.outsource.resource'
    _rec_name = 'identifier'
    _description = 'Resource'
    _inherit = ['mail.thread']

    # BASIC FIELDS
    # ----------------------------------------------------------
    # TODO MAKE THIS AUTOINCREMENTING
    identifier = fields.Char()

    name = fields.Char()
    type = fields.Char()
    type_class = fields.Char()
    agency_ref_num = fields.Char()
    emp_num = fields.Char()
    date_of_join = fields.Date()
    date_of_last_working_day = fields.Date()
    has_tool_or_uniform = fields.Boolean()

    # RELATIONSHIPS
    # ----------------------------------------------------------
    contractor_id = fields.Many2one('budget.contractor.contractor', string='Contractor')

    # POLYMORPH
    # ----------------------------------------------------------
    # @api.multi
    # def name_get(self):
    #     result = []
    #     for r in self:
    #         result.append((r.id, "%s:%s" % (r.contractor_id.alias, r.name)))
    #     return result
