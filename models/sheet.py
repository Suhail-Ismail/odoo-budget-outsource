# -*- coding: utf-8 -*-
from odoo import models, fields, api

from odoo.exceptions import ValidationError
from ..creator import SBH, DATASHEET


class Sheet(models.Model):
    _name = 'budget.outsource.sheet'
    _rec_name = 'name'
    _description = 'Sheet'
    _inherit = ['budget.enduser.mixin']

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------

    name = fields.Char()
    type = fields.Char()
    total_required_hours = fields.Integer()
    period_start = fields.Date()
    period_end = fields.Date()
    ramadan_start = fields.Date()
    ramadan_end = fields.Date()

    # RELATIONSHIPS
    # ----------------------------------------------------------
    po_id = fields.Many2one('budget.purchase.order', string='Purchase Order')
    contractor_id = fields.Many2one('budget.contractor.contractor', string='Contractor')

    # BUTTONS
    # ----------------------------------------------------------
