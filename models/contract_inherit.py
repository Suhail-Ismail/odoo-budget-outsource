# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Contract(models.Model):
    _inherit = 'budget.contractor.contract'

    is_resource = fields.Boolean('Is Resource', default=False)
