# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Position(models.Model):
    _name = 'budget.outsource.position'
    _rec_name = 'os_ref'
    _description = 'Position'

    # BASIC FIELDS
    # ----------------------------------------------------------

    os_ref = fields.Char()
    name = fields.Char()
    level = fields.Char()
    revise_rate = fields.Monetary(currency_field='currency_id', default=0.00)

    capex_percent = fields.Integer(default=0)
    opex_percent = fields.Integer(default=0)
    revenue_percent = fields.Integer(default=0)

    # RELATIONSHIPS
    # ----------------------------------------------------------
    currency_id = fields.Many2one('res.currency', readonly=True,
                                  default=lambda self: self.env.user.company_id.currency_id)
    po_id = fields.Many2one('budget.purchase.order', string='Purchase Order')

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    unit_rate = fields.Monetary(currency_field='currency_id',
                                default=0.00,
                                digits=(12, 2),
                                compute='_compute_unit_rate',
                                store=True)

    rate = fields.Monetary(currency_field='currency_id',
                           default=0.00,
                           digits=(12, 2),
                           compute='_compute_rate',
                           store=True)

    rate_diff_percent = fields.Monetary(currency_field='currency_id',
                                        default=0.00,
                                        digits=(12, 4),
                                        compute='_compute_rate_diff_percent',
                                        store=True)

    @api.one
    @api.depends('name', 'level', 'po_id')
    def _compute_unit_rate(self):
        if self.name and self.level and self.po_id.mapped('contractor_id'):
            unit_rate_id = self.env['budget.outsource.unit.rate'].search([
                ('position_name', '=', self.name),
                ('position_level', '=', self.level),
                ('contractor_id', '=', self.po_id.contractor_id.id)
            ])
            self.unit_rate = unit_rate_id.amount

        else:
            self.unit_rate = 0.0

    @api.one
    @api.depends('unit_rate', 'revise_rate')
    def _compute_rate(self):
        self.rate = self.revise_rate if self.revise_rate > 0 else self.unit_rate

    @api.one
    @api.depends('unit_rate', 'rate')
    def _compute_rate_diff_percent(self):
        self.rate_diff_percent = ((self.rate - self.unit_rate) / self.unit_rate) * 100
