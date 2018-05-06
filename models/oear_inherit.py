# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Oear(models.Model):
    _inherit = 'budget.opex.oear'

    is_resource = fields.Boolean('Is Resource', default=False)
