# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Invoice(models.Model):
    _name = 'outsource.invoice'
    _rec_name = 'po_num'
    _description = 'Invoice'

    # BASIC FIELDS
    # ----------------------------------------------------------
    invoice_date = fields.Date()
    invoice_hour = fields.Float(default=0.00)
    invoice_claim = fields.Float(default=0.00)
    invoice_cert_amount = fields.Float(default=0.00)
    remarks = fields.Text()

    resource_id = fields.Many2one('outsource.resource')
    po_line_detail_id = fields.Many2one('outsource.purchase.order.line.detail')