# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Contract(models.Model):
    _inherit = 'budget.contractor.contract'

    # BASIC FIELDS
    # ----------------------------------------------------------
    # TODO DEPRECATED
    is_resource = fields.Boolean('Is Resource', default=False)

    is_outsource = fields.Boolean('Is Resource', default=False)
