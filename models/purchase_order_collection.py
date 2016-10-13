# -*- coding: utf-8 -*-

from .utils import choices_tuple
from openerp import models, fields, api

class PurchaseOrderCollection(models.Model):
    _name = 'outsource.purchase.order.collection'
    _rec_name = 'po_num'
    _description = 'Purchase Order Collection'
    # _order = 'po_date desc, po_num'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    # CHOICES
    # ----------------------------------------------------------
    STATES = choices_tuple(['active', 'closed'], is_sorted=False)

    # BASIC FIELDS
    # ----------------------------------------------------------

    # RELATIONSHIPS
    # ----------------------------------------------------------
    po_ids = fields.One2many('outsource.purchase.order', 'po_collection_id', string="PO Collections")
    contractor_id = fields.Many2one('res.partner',
                                    compute='_compute_contractor_id',
                                    string='Contractor')
    # COMPUTED FIELDS
    # ----------------------------------------------------------
    state = fields.Selection(compute='_compute_state', selection=STATES)

    po_num = fields.Char(compute='_compute_po_num', string='Purchase Order' )
    po_date = fields.Date(compute='_compute_po_date', string='Starting Date' )
    po_value = fields.Float(compute='_compute_po_value', string='PO Value', digits=(32, 2) )
    capex_commitment_value = fields.Float(compute='_compute_capex_commitment_value', string='CAPEX Commitment', digits=(32, 2))
    capex_expenditure_value = fields.Float(compute='_compute_capex_expenditure_value', string='CAPEX Expenditure', digits=(32, 2))
    opex_value = fields.Float(compute='_compute_opex_value', string='OPEX Value', digits=(32, 2))
    revenue_value = fields.Float(compute='_compute_revenue_value', string='Revenue Value', digits=(32, 2))
    task_num = fields.Char(compute='_compute_task_num', string='Task Number')
    status = fields.Char(compute='_compute_status', string='Status')
    remarks = fields.Text(compute='_compute_remarks')
    type = fields.Char(compute='_compute_type', string='Type')

    total_approval = fields.Integer(compute='_compute_total_approval')
    total_po_line = fields.Integer(compute='_compute_total_po_line')
    total_po_line_detail = fields.Integer(compute='_compute_total_po_line_detail')
    total_claim = fields.Integer(compute='_compute_total_claim')
    total_resource = fields.Integer(compute='_compute_total_resource')
    total_non_mobilize = fields.Integer(compute='_compute_total_non_mobilize')

    @api.one
    @api.depends('state')
    def _compute_state(self):
        if 'active' in self.po_ids.mapped('state'):
            self.state = 'active'
        else:
            self.state = 'closed'

    @api.one
    @api.depends('po_ids')
    def _compute_po_num(self):
        if self.po_ids:
            self.po_num = self.mapped('po_ids.po_num')[-1]

    @api.one
    @api.depends('po_ids')
    def _compute_po_date(self):
        if self.po_ids:
            self.po_date = self.mapped('po_ids.po_date')[-1]

    @api.one
    @api.depends('po_ids')
    def _compute_po_value(self):
        if self.po_ids:
            self.po_value = sum(self.mapped('po_ids.po_value'))

    @api.one
    @api.depends('po_ids')
    def _compute_contractor_id(self):
        if self.po_ids:
            self.contractor_id = self.mapped('po_ids.contractor_id')[-1]

    @api.one
    @api.depends('po_ids')
    def _compute_capex_commitment_value(self):
        if self.po_ids:
            self.capex_commitment_value = sum(self.mapped('po_ids.capex_commitment_value'))

    @api.one
    @api.depends('po_ids')
    def _compute_capex_expenditure_value(self):
        if self.po_ids:
            self.capex_expenditure_value = sum(self.mapped('po_ids.capex_expenditure_value'))

    @api.one
    @api.depends('po_ids')
    def _compute_opex_value(self):
        if self.po_ids:
            self.opex_value = sum(self.mapped('po_ids.opex_value'))

    @api.one
    @api.depends('po_ids')
    def _compute_revenue_value(self):
        if self.po_ids:
            self.revenue_value = sum(self.mapped('po_ids.revenue_value'))

    @api.one
    @api.depends('po_ids')
    def _compute_task_num(self):
        if self.po_ids:
            self.task_num = self.mapped('po_ids.task_num')[-1]

    @api.one
    @api.depends('po_ids')
    def _compute_status(self):
        if self.po_ids:
            self.status = self.mapped('po_ids.status')[-1]

    @api.one
    @api.depends('po_ids')
    def _compute_remarks(self):
        if self.po_ids:
            self.remarks = self.mapped('po_ids.remarks')[-1]

    @api.one
    @api.depends('po_ids')
    def _compute_type(self):
        if self.po_ids:
            self.type = self.mapped('po_ids.type')[-1]

    @api.one
    @api.depends('po_ids')
    def _compute_total_approval(self):
        self.total_approval = len(self.mapped('po_ids.approval_ids'))

    @api.one
    @api.depends('po_ids')
    def _compute_total_po_line(self):
        self.total_po_line = len(self.mapped('po_ids.po_line_ids'))

    @api.one
    @api.depends('po_ids')
    def _compute_total_claim(self):
        self.total_claim = 0

    @api.one
    @api.depends('po_ids')
    def _compute_total_resource(self):
        self.total_resource = len(self.mapped(
            'po_ids.po_line_ids.po_line_detail_ids.resource_ids'))

    @api.one
    @api.depends('po_ids')
    def _compute_total_non_mobilize(self):
        self.total_non_mobilize = sum(self.mapped('po_ids.total_non_mobilize'))

    @api.one
    @api.depends('po_ids')
    def _compute_total_po_line_detail(self):
        self.total_po_line_detail = len(self.mapped('po_ids.po_line_detail_ids'))

    # RELATIONSHIPS COMPUTED FIELDS
    # ----------------------------------------------------------
    approval_ids = fields.One2many('outsource.approval',
                                   'po_id',
                                   compute="_compute_o2m_approval_ids"
                                   )
    po_line_ids = fields.One2many('outsource.purchase.order.line',
                                  compute="_compute_o2m_po_line_ids",
                                  )
    po_line_detail_ids = fields.One2many('outsource.purchase.order.line.detail',
                                             compute="_compute_o2m_po_line_detail_ids",
                                             )
    resource_ids = fields.One2many('res.partner',
                                   compute="_compute_o2m_resource_ids",
                                   )

    @api.depends('approval_ids')
    def _compute_o2m_approval_ids(self):
        self.approval_ids = self.mapped('po_ids.approval_ids')

    @api.depends('po_line_ids')
    def _compute_o2m_po_line_ids(self):
        self.po_line_ids = self.mapped('po_ids.po_line_ids')

    @api.depends('po_line_detail_ids')
    def _compute_o2m_po_line_detail_ids(self):
        self.po_line_detail_ids = self.mapped('po_ids.po_line_detail_ids')

    @api.depends('resource_ids')
    def _compute_o2m_resource_ids(self):
        self.resource_ids = self.mapped('po_line_ids.po_line_detail_ids.resource_ids')

    # BUTTON ACTIONS / TRANSITIONS
    # ----------------------------------------------------------
    @api.one
    def set2close(self):
        import ipdb;        ipdb.set_trace()