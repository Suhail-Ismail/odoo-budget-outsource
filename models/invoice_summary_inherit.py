# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InvoiceSummary(models.Model):
    _inherit = 'budget.invoice.invoice.summary'

    # BASIC FIELDS
    # ----------------------------------------------------------
    # TODO DEPRECATED
    is_resource = fields.Boolean('Is Resource', default=False)

    is_outsource = fields.Boolean('Is Resource', default=False)

    @api.onchange('objective')
    def _onchange_invoice_ids_filter(self):
        res = super(InvoiceSummary, self)._onchange_invoice_ids_filter()
        res['domain']['invoice_ids'].append(
            ('is_outsource', '=', self.is_outsource)
        )
        return res
