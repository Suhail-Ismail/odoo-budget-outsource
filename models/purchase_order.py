# -*- coding: utf-8 -*-
from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _name = 'outsource.purchase.order'
    _rec_name = 'po_num'
    _description = 'Purchase Order'

    # BASIC FIELDS
    # ----------------------------------------------------------
    po_num = fields.Char(string='Purchase Order')
    po_date = fields.Date(string='PO Date')
    po_value = fields.Float(string='PO Value', digits=(32, 2), default=0.00)
    contractor = fields.Char(string='Contractor')
    budget = fields.Char(string='Budget')
    capex_commitment_value = fields.Float(string='CAPEX Commitment', digits=(32, 2), default=0.00)
    capex_expenditure_value = fields.Float(string='CAPEX Expenditure', digits=(32, 2), default=0.00)
    opex_value = fields.Float(string='OPEX Value', digits=(32, 2), default=0.00)
    revenue_value = fields.Float(string='Revenue Value', digits=(32, 2), default=0.00)
    task_num = fields.Char(string='Task Number')

    renew_status = fields.Char(string='Renew Status')
    renew_po_no = fields.Char(string='Renew PO No')
    po_status = fields.Char(string='PO Status')
    po_remarks = fields.Text(string='PO Remarks')
    po_type = fields.Char(string='PO Type')
