# -*- coding: utf-8 -*-
from .utils import choices_tuple
from openerp import models, fields, api


class Contractor(models.Model):
    _name = 'outsource.contractor'
    _rec_name = 'name'
    _description = 'Contractor'

    alias = fields.Char(string="Alias")
    name = fields.Char(string="Name")

    street = fields.Char(string="Street")
    street2 = fields.Char(string="Street2")
    city = fields.Char(string="City")
    website = fields.Char(string="Website")
    # image = fields.Binary("Image", attachment=True,
    #     help="This field holds the image used as avatar for this contact, limited to 1024x1024px",
    #     default=lambda self: self._get_default_image(False, True))

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
    resource_ids = fields.One2many('outsource.resource',
                             'contractor_id',
                             string="Resources")
    contact_ids = fields.One2many('outsource.contractor.contact',
                             'contractor_id',
                             string="Contacts")
    # COMPUTE FIELDS
    # ----------------------------------------------------------
    total_approval = fields.Integer(compute='_compute_total_approval', store=True)
    total_po = fields.Integer(compute='_compute_total_po', store=True)
    total_resource = fields.Integer(compute='_compute_total_resource', store=True)
    total_po_line_detail = fields.Integer(compute='_compute_total_po_line_detail', store=True)
    total_non_mobilize = fields.Integer(compute='_compute_total_non_mobilize', store=True)
    total_invoice = fields.Integer(compute='_compute_total_invoice', store=True)

    po_line_detail_ids = fields.One2many('outsource.purchase.order.line.detail',
                                         compute="_compute_o2m_po_line_detail_ids",
                                         )

    @api.one
    @api.depends('total_approval', 'approval_ids')
    def _compute_total_approval(self):
        self.total_approval = len(self.mapped('approval_ids'))

    @api.one
    @api.depends('total_po', 'po_ids')
    def _compute_total_po(self):
        self.total_po = len(self.mapped('po_ids'))

    @api.one
    @api.depends('total_resource', 'resource_ids')
    def _compute_total_resource(self):
        self.total_resource = len(self.mapped('resource_ids'))

    @api.one
    @api.depends('total_po_line_detail', 'po_ids.po_line_ids.po_line_detail_ids')
    def _compute_total_po_line_detail(self):
        self.total_po_line_detail = len(self.mapped('po_ids.po_line_ids.po_line_detail_ids'))

    @api.one
    @api.depends('total_non_mobilize', 'total_po_line_detail', 'total_resource')
    def _compute_total_non_mobilize(self):
        self.total_non_mobilize = self.total_po_line_detail - self.total_resource

    @api.one
    @api.depends('total_resource', 'resource_ids')
    def _compute_total_invoice(self):
        self.total_resource = self.mapped('resource_ids')

    @api.one
    @api.depends('po_line_detail_ids', 'po_ids.po_line_ids.po_line_detail_ids')
    def _compute_o2m_po_line_detail_ids(self):
        self.po_line_detail_ids = self.mapped('po_ids.po_line_ids.po_line_detail_ids')


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
    contractor_id = fields.Many2one('outsource.contractor', string='Contractor')


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
    contractor_id = fields.Many2one('outsource.contractor', string='Contractor')
