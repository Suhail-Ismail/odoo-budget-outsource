# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InvoiceSummary(models.Model):
    _inherit = 'budget.invoice.invoice.summary'

    # BASIC FIELDS
    # ----------------------------------------------------------
    is_resource = fields.Boolean('Is Resource', default=False)
