# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import ValidationError
from .utils import choices_tuple

class PurchaseOrder(models.Model):
    _name = 'outsource.purchase.order'
    _rec_name = 'po_num'
    _description = 'Purchase Order'
#    _order = 'id'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    # CHOICES
    # ----------------------------------------------------------
    STATES = choices_tuple(['active', 'closed'], is_sorted=False)
    BUDGET_TYPES = choices_tuple(['capex', 'opex', 'revenue'])

    # BASIC FIELDS
    # ----------------------------------------------------------
    state = fields.Selection(STATES, default='active')

    # BASIC FIELDS
    # ----------------------------------------------------------
    budget_type = fields.Selection(BUDGET_TYPES)
    po_num = fields.Char(string='Purchase Order')
    po_date = fields.Date(string='PO Date')
    po_value = fields.Float(string='PO Value', digits=(32, 2), default=0.00)
    capex_commitment_value = fields.Float(string='CAPEX Commitment', digits=(32, 2), default=0.00)
    capex_expenditure_value = fields.Float(string='CAPEX Expenditure', digits=(32, 2), default=0.00)
    opex_value = fields.Float(string='OPEX Value', digits=(32, 2), default=0.00)
    revenue_value = fields.Float(string='Revenue Value', digits=(32, 2), default=0.00)
    task_num = fields.Char(string='Task Number')
    # status = fields.Char(string='Status')
    remarks = fields.Text()
    type = fields.Char(string='Type')

    # MISC FIELDS
    # ----------------------------------------------------------
    renewed_date = fields.Date(string='Renewal Date')

    # RELATIONSHIPS
    # ----------------------------------------------------------
    # task_ids = fields.One2many('outsource.task', 'po_id', string="Tasks")
    approval_ids = fields.One2many('outsource.approval', 'po_id', string="Approvals")
    po_line_ids = fields.One2many('outsource.purchase.order.line', 'po_id', string="Purchase Order Lines")
    invoice_ids = fields.One2many('outsource.invoice', 'po_id', string="Invoices")
    po_collection_id = fields.Many2one('outsource.purchase.order.collection', string='PO Collection')
    contractor_id = fields.Many2one('res.partner', string='Contractor')

    # self reference, one new po to many renewals
    renewed_po_ids = fields.One2many('outsource.purchase.order', 'new_po_id', string="Renewals")
    new_po_id = fields.Many2one('outsource.purchase.order', string='Renewed PO')

    # CONSTRAINTS
    # ----------------------------------------------------------
    _sql_constraints = [
        (
            '_uniq_po_num',
            'UNIQUE(po_num)',
            'PO Number must be unqiue!',
            ),
    ]

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    total_approval = fields.Integer(compute='_compute_total_approval', store=True)
    total_po_line = fields.Integer(compute='_compute_total_po_line', store=True)
    total_po_line_detail = fields.Integer(compute='_compute_total_po_line_detail', store=True)
    total_invoice = fields.Integer(compute='_compute_total_invoice', store=True)
    total_resource = fields.Integer(compute='_compute_total_resource', store=True)
    total_non_mobilize = fields.Integer(compute='_compute_total_non_mobilize', store=True)

    po_line_detail_ids = fields.One2many('outsource.purchase.order.line.detail',
                                         '_compute_po_line_detail_po_id',
                                         compute="_compute_o2m_po_line_detail_ids",
                                         string="Po Line Details",
                                         store=True
                                         )

    resource_ids = fields.One2many('res.partner',
                                   '_compute_resource_po_id',
                                   compute="_compute_o2m_resource_ids",
                                   string="Resources",
                                   store=True
                                   )
    @api.one
    @api.depends('approval_ids')
    def _compute_total_approval(self):
        self.total_approval = len(self.mapped('approval_ids'))

    @api.one
    @api.depends('po_line_ids')
    def _compute_total_po_line(self):
        self.total_po_line = len(self.mapped('po_line_ids'))

    @api.one
    @api.depends('total_invoice')
    def _compute_total_invoice(self):
        self.total_invoice = 0

    @api.one
    @api.depends('po_line_ids.po_line_detail_ids.position_history_ids.resource_id')
    def _compute_total_resource(self):
        self.total_resource = len(self.mapped('po_line_ids.po_line_detail_ids.position_history_ids.resource_id'))

    @api.one
    @api.depends('total_po_line_detail', 'po_line_ids.po_line_detail_ids.mobilize_status')
    def _compute_total_non_mobilize(self):
        mobilize = self.mapped('po_line_ids.po_line_detail_ids.mobilize_status').count('mobilized')
        self.total_non_mobilize = self.total_po_line_detail - mobilize

    @api.one
    @api.depends('po_line_ids.po_line_detail_ids')
    def _compute_total_po_line_detail(self):
        self.total_po_line_detail = len(self.mapped('po_line_ids.po_line_detail_ids'))

    @api.one
    @api.depends('po_line_ids.po_line_detail_ids')
    def _compute_o2m_po_line_detail_ids(self):
        self.po_line_detail_ids = self.mapped('po_line_ids.po_line_detail_ids')

    @api.one
    @api.depends('po_line_ids.po_line_detail_ids.position_history_ids.resource_id')
    def _compute_o2m_resource_ids(self):
        self.resource_ids = self.mapped('po_line_ids.po_line_detail_ids.position_history_ids.resource_id')

    # BUTTON ACTIONS / TRANSITIONS
    # ----------------------------------------------------------
    @api.one
    def set2close(self):
        import ipdb; ipdb.set_trace()

    @api.model
    @api.returns('self', lambda rec: rec.id)
    def create(self, values):
        new_po_id = values.get('new_po_id', False)
        if new_po_id:
            po = self.env['outsource.purchase.order'].search([('new_po_id', '=', new_po_id)])
            values['po_collection_id'] = po[0].po_collection_id.id
        return super(PurchaseOrder, self).create(values)

    @api.multi
    def write(self, values):
        # Links Previous PO to new_po
        new_po_id = values.get('new_po_id', False)
        if new_po_id:
            values['po_collection_id'] = self.new_po_id.po_collection_id.id
        return super(PurchaseOrder, self).write(values)


class PurchaseOrderLine(models.Model):
    _name = 'outsource.purchase.order.line'
    _description = 'Purchase Order Line'

    @api.multi
    def name_get(self):
        result = []
        for r in self:
            result.append((
                r.id,
                u"%s\%s" % (r.po_id.po_num, r.line_num)
            ))
        return result

    line_num = fields.Char(string='Line Number')
    line_duration = fields.Integer(string='Duration', default=0)
    line_value = fields.Float(string='Value', digits=(32, 2), default=0.00)
    line_revise_rate = fields.Float(string='Revise Rate Value', digits=(32, 2), default=0.00)
    line_rate = fields.Float(string='Rate', digits=(32, 2), default=0.00)
    line_status = fields.Char(string='Status')
    line_actuals = fields.Float(string='Actual Value', digits=(32, 2), default=0.00)
    capex_percent = fields.Float(string='Capex %', digits=(32, 2), default=0.00)
    opex_percent = fields.Float(string='Opex %', digits=(32, 2), default=0.00)
    revenue_percent = fields.Float(string='Revenue %', digits=(32, 2), default=0.00)

    # RELATIONSHIPS
    # ----------------------------------------------------------
    po_id = fields.Many2one('outsource.purchase.order', string='Purchase Order')
    po_line_detail_ids = fields.One2many('outsource.purchase.order.line.detail',
                                  'po_line_id',
                                  string="Line Details")

class PurchaseOrderLineDetail(models.Model):
    _name = 'outsource.purchase.order.line.detail'
    _rec_name = 'job_id'
    _description = 'Purchase Order Line Detail'

    # BASIC FIELDS
    # ----------------------------------------------------------
    job_id = fields.Char(string='Job ID')
    position = fields.Char(string='Position')
    level = fields.Char(string='Level')
    rate = fields.Float(string='Rate', digits=(32, 2), default=0.00)
    revise_rate = fields.Float(string='Revise Rate', digits=(32, 2), default=0.00)
    division = fields.Char(string='Division')
    section = fields.Char(string='Section')
    sub_section = fields.Char(string='Sub Section')
    director_name = fields.Char(string='Director Name')
    frozen_status = fields.Char(string='Frozen Status')
    approval_ref_num = fields.Char(string='Approval Ref No')
    approval_reason = fields.Text()
    kpi_2016 = fields.Char(string='KPI 2016')
    capex_percent = fields.Float(string='Capex Percent', digits=(32, 2), default=0.00)
    opex_percent = fields.Float(string='Opex Percent', digits=(32, 2), default=0.00)
    revenue_percent = fields.Float(string='Revenue Percent', digits=(32, 2), default=0.00)
    rate_diff_percent = fields.Float(string='Rate Variation', digits=(32, 2), default=0.00)

    # RELATIONSHIPS
    # ----------------------------------------------------------
    po_line_id = fields.Many2one('outsource.purchase.order.line', string='Purchase Order Line')
    resource_ids = fields.One2many('res.partner',
                             'po_line_detail_id',
                             string="Resource")
    position_history_ids = fields.One2many('outsource.position.history',
                                   'po_line_detail_id',
                                   string="Position History")
    # COMPUTE FIELD REFERENCES
    # ----------------------------------------------------------
    _compute_po_line_detail_po_id = fields.Many2one('outsource.purchase.order', string='Compute Purchase Order')

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    mobilize_status = fields.Char(compute='_compute_mobilize_status', store=True)

    @api.one
    @api.depends('position_history_ids.status')
    def _compute_mobilize_status(self):
        # mobilized; new; vacant
        # If total number of position history is 0 it means it is new

        if len(self.position_history_ids) == 0:
            self.mobilize_status = 'new'

        # If total number of position history is more than 1 it means it is vacant or mobilized
        else:
            for record in self.position_history_ids:
                self.mobilize_status = 'vacant'

                if record.status == 'active':
                    self.mobilize_status = 'mobilized'
                    break

    # # CONSTRAINS
    # # ----------------------------------------------------------
    # @api.constrains('position_history_ids')
    # def _check_status(self):
    #     count = 0
    #     for r in self.position_history_ids:
    #         if r.status == 'active':
    #             count += 1
    #
    #     if count > 1:
    #         raise models.ValidationError('Only 1 Resource can be active per position')
    #
