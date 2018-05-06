# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Contract(models.Model):
    _inherit = 'budget.contractor.contract'

    is_outsource = fields.Boolean('Is Outsource', default=False)
