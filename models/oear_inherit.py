# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Oear(models.Model):
    _inherit = 'budget.opex.oear'

    is_outsource = fields.Boolean('Is Outsource', default=False)
