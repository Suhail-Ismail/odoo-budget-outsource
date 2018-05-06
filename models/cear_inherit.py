# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Cear(models.Model):
    _inherit = 'budget.capex.cear'

    is_resource = fields.Boolean('Is Resource', default=False)
