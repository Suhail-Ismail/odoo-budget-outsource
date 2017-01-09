# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Contractor(models.Model):
    _inherit = 'res.partner'

    # RELATIONSHIPS
    # ----------------------------------------------------------
    unit_rate_ids = fields.One2many('outsource.unit.rate',
                                  'contractor_id',
                                  string="Unit Rates")
    approval_ids = fields.One2many('outsource.approval',
                                    'contractor_id',
                                    string="Approvals")
    po_ids = fields.One2many('outsource.purchase.order',
                                    'contractor_id',
                                    string="Purchase Orders")
    resource_ids = fields.One2many('res.partner',
                             'contractor_id',
                             string="Resources")
    claim_ids = fields.One2many('outsource.claim',
                             'contractor_id',
                             string="Resources")
    # COMPUTE FIELDS
    # ----------------------------------------------------------
    total_approval = fields.Integer(compute='_compute_total_approval')
    total_po = fields.Integer(compute='_compute_total_po')
    total_resource = fields.Integer(compute='_compute_total_resource')
    total_po_line_detail = fields.Integer(compute='_compute_total_po_line_detail')
    total_non_mobilize = fields.Integer(compute='_compute_total_non_mobilize')
    total_claim = fields.Integer(compute='_compute_total_claim')
    po_line_detail_ids = fields.One2many('outsource.purchase.order.line.detail',
                                         compute="_compute_o2m_po_line_detail_ids",
                                         )

    @api.one
    @api.depends('po_ids')
    def _compute_total_non_mobilize(self):
        positions = self.mapped('po_ids.po_line_ids.po_line_detail_ids')
        self.total_non_mobilize = len([r for r in positions if not r.mobilize_status == 'mobilized'])

    @api.one
    @api.depends('resource_ids')
    def _compute_total_resource(self):
        self.total_resource = len(self.mapped('resource_ids'))

    @api.one
    @api.depends('po_ids')
    def _compute_total_po_line_detail(self):
        self.total_po_line_detail = len(self.mapped('po_ids.po_line_ids.po_line_detail_ids'))

    @api.one
#    @api.depends('claim_ids')
    def _compute_total_claim(self):
        self.total_claim = 0

    @api.one
    @api.depends('po_ids')
    def _compute_total_po(self):
        self.total_po = len(self.mapped('po_ids'))

    @api.one
    @api.depends('approval_ids')
    def _compute_total_approval(self):
        self.total_approval = len(self.mapped('approval_ids'))

    @api.one
    @api.depends('po_line_detail_ids', 'po_ids.po_line_ids.po_line_detail_ids')
    def _compute_o2m_po_line_detail_ids(self):
        self.po_line_detail_ids = self.mapped('po_ids.po_line_ids.po_line_detail_ids')


    # CONSTRAINS
    # ----------------------------------------------------------
    @api.constrains('unit_rate_ids')
    def _check_unit_rate_ids(self):
        positions = self.unit_rate_ids.mapped('position')
        if len(positions) != len(set(positions)):
            raise ValidationError('Position in Unit Rate Must be unique')


