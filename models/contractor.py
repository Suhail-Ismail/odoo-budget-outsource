# -*- coding: utf-8 -*-
from .utils import choices_tuple
from openerp import models, fields, api
from openerp.exceptions import ValidationError

class Contractor(models.Model):
    _inherit = 'res.partner'
    _rec_name = 'name'
    _description = 'Contractor'

    alias = fields.Char(string="Alias")
    is_contractor = fields.Boolean(string="Contractor")

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
    contact_ids = fields.One2many('outsource.contractor.contact',
                             'contractor_id',
                             string="Contacts")
    invoice_ids = fields.One2many('outsource.invoice',
                             'contractor_id',
                             string="Resources")
    # COMPUTE FIELDS
    # ----------------------------------------------------------
    total_approval = fields.Integer(compute='_compute_total_approval')
    total_po = fields.Integer(compute='_compute_total_po')
    total_resource = fields.Integer(compute='_compute_total_resource')
    total_po_line_detail = fields.Integer(compute='_compute_total_po_line_detail')
    total_non_mobilize = fields.Integer(compute='_compute_total_non_mobilize')
    total_invoice = fields.Integer(compute='_compute_total_invoice')
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
#    @api.depends('invoice_ids')
    def _compute_total_invoice(self):
        self.total_invoice = 0

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

class ContractorContact(models.Model):
    _name = 'outsource.contractor.contact'
    _rec_name = 'name'
    _order = 'name'
    _description = 'Contractor Contact'

    # BASIC FIELDS
    # ----------------------------------------------------------
    name = fields.Char(string="Name")
    job_position = fields.Char(string="Position")
    is_spoc = fields.Boolean(string="Is SPOC")
    phone = fields.Char(string="Phone")
    mobile = fields.Char(string="Mobile")
    email = fields.Char(string="E-Mail")

    # RELATIONSHIPS
    # ----------------------------------------------------------
    contractor_id = fields.Many2one('res.partner', string='Contractor')


class UnitRate(models.Model):
    _name = 'outsource.unit.rate'
    _rec_name = 'position'
    _description = 'Unit Rate'

    POSITIONS = choices_tuple(['labor', 'driver', 'technician', 'rigger', 'associate engineer',
                               'engineer', 'senior engineer', 'expert engineer', 'car'])

    # BASIC FIELDS
    # ----------------------------------------------------------
    position = fields.Selection(string='Position', selection=POSITIONS)
    level_1 = fields.Float(string='Level 1', digits=(32, 2), default=0.00)
    level_2 = fields.Float(string='Level 2', digits=(32, 2), default=0.00)
    level_3 = fields.Float(string='Level 3', digits=(32, 2), default=0.00)
    level_4 = fields.Float(string='Level 4', digits=(32, 2), default=0.00)
    percent = fields.Float(string='Percent', digits=(32, 2), default=0.00)

    # RELATIONSHIPS
    # ----------------------------------------------------------
    contractor_id = fields.Many2one('res.partner', string='Contractor')
