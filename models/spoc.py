# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Spoc(models.Model):
    _name = 'budget.outsource.spoc'
    _rec_name = 'name'
    _description = 'Single Point Of Contact'
    _inherit = ['budget.enduser.mixin']

    name = fields.Char()
    email = fields.Char()
    contact = fields.Char()

    # RELATIONSHIPS
    # ----------------------------------------------------------
