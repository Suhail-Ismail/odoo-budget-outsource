# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Invoice(models.Model):
    _inherit = 'budget.invoice.invoice'

    is_resource = fields.Boolean('Is Resource', default=False)

    # BASIC FIELDS
    # ----------------------------------------------------------
    outsource_actual_hour = fields.Float(default=0.00)
    outsource_claim_hour = fields.Float(default=0.00)

    # RELATIONSHIPS
    # ----------------------------------------------------------
    mobilize_id = fields.Many2one('budget.outsource.mobilize')
    position_id = fields.Many2one('budget.outsource.position')
