# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Invoice(models.Model):
    _name = 'outsource.invoice'
    _rec_name = 'invoice_date'

    # BASIC FIELDS
    # ----------------------------------------------------------
    invoice_date = fields.Date(string='Invoice Date')
    invoice_hour = fields.Float(string='Invoice Hour', digits=(32, 2), default=0.00)
    invoice_claim = fields.Float(string='Invoice Claim', digits=(32, 2), default=0.00)
    invoice_cert_amount = fields.Float(string='Certified Amount', digits=(32, 2), default=0.00)
    remarks = fields.Text()

    # RELATIONSHIPS
    # ----------------------------------------------------------
    resource_id = fields.Many2one('outsource.resource', string='Resource')
    approval_ids = fields.One2many('outsource.approval', 'po_id', string="Approvals")


class Period(models.Model):
    _name = 'outsource.invoice.period'
    _rec_name = 'remarks'

    # BASIC FIELDS
    # ----------------------------------------------------------
    period_start = fields.Date(string='Period Start')
    period_end = fields.Date(string='Period End')
    ramadan_start = fields.Date(string='Ramadan Start')
    ramadan_end = fields.Date(string='Ramadan End')
    remarks = fields.Date(string='Remarks')
