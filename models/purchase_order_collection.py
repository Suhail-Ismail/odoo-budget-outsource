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

    # COMPUTED FIELDS
    # ----------------------------------------------------------
    state = fields.Selection(compute='_compute_state', selection=STATES)

    po_num = fields.Char(compute='_compute_po_num', string='Purchase Order' )
    po_date = fields.Date(compute='_compute_po_date', string='Starting Date' )
    po_value = fields.Float(compute='_compute_po_value', string='PO Value', digits=(32, 2) )
    contractor = fields.Char(compute='_compute_po_contractor', string='Contractor' )
    capex_commitment_value = fields.Float(compute='_compute_capex_commitment_value', string='CAPEX Commitment', digits=(32, 2))
    capex_expenditure_value = fields.Float(compute='_compute_capex_expenditure_value', string='CAPEX Expenditure', digits=(32, 2))
    opex_value = fields.Float(compute='_compute_opex_value', string='OPEX Value', digits=(32, 2))
    revenue_value = fields.Float(compute='_compute_revenue_value', string='Revenue Value', digits=(32, 2))
    task_num = fields.Char(compute='_compute_task_num', string='Task Number')
    status = fields.Char(compute='_compute_status', string='Status')
    remarks = fields.Text(compute='_compute_remarks')
    type = fields.Char(compute='_compute_type', string='Type')

    @api.depends('state', 'po_ids')
    def _compute_state(self):
        if 'active' in self.po_ids.mapped('state'):
            self.state = 'active'
        else:
            self.state = 'closed'

    @api.depends('po_num', 'po_ids')
    def _compute_po_num(self):
        if self.po_ids:
            self.po_num = self.po_ids.filtered(lambda r: not r.is_renewed).po_num

    @api.depends('po_date', 'po_ids')
    def _compute_po_date(self):
        if self.po_ids:
            self.po_date = self.po_ids.filtered(lambda r: not r.is_renewed).po_date

    @api.depends('po_value', 'po_ids')
    def _compute_po_value(self):
        if self.po_ids:
            self.po_value = sum(self.po_ids.mapped('po_value'))

    @api.depends('po_date', 'po_ids')
    def _compute_po_contractor(self):
        if self.po_ids:
            self.contractor = self.po_ids.filtered(lambda r: not r.is_renewed).contractor

    @api.depends('capex_commitment_value', 'po_ids')
    def _compute_capex_commitment_value(self):
        if self.po_ids:
            self.capex_commitment_value = sum(self.po_ids.mapped('capex_commitment_value'))

    @api.depends('capex_expenditure_value', 'po_ids')
    def _compute_capex_expenditure_value(self):
        if self.po_ids:
            self.capex_expenditure_value = sum(self.po_ids.mapped('capex_expenditure_value'))

    @api.depends('opex_value', 'po_ids')
    def _compute_opex_value(self):
        if self.po_ids:
            self.opex_value = sum(self.po_ids.mapped('opex_value'))

    @api.depends('revenue_value', 'po_ids')
    def _compute_revenue_value(self):
        if self.po_ids:
            self.revenue_value = sum(self.po_ids.mapped('revenue_value'))

    @api.depends('task_num', 'po_ids')
    def _compute_task_num(self):
        if self.po_ids:
            self.task_num = self.po_ids.filtered(lambda r: not r.is_renewed).task_num

    @api.depends('status', 'po_ids')
    def _compute_status(self):
        if self.po_ids:
            self.status = self.po_ids.filtered(lambda r: not r.is_renewed).status

    @api.depends('remarks', 'po_ids')
    def _compute_remarks(self):
        if self.po_ids:
            self.remarks = self.po_ids.filtered(lambda r: not r.is_renewed).remarks

    @api.depends('type', 'po_ids')
    def _compute_type(self):
        if self.po_ids:
            self.type = self.po_ids.filtered(lambda r: not r.is_renewed).type

    # RELATIONSHIPS COMPUTED FIELDS
    # ----------------------------------------------------------
    approval_ids = fields.One2many('outsource.approval',
                                   'po_id',
                                   compute="_compute_o2m_all_approval_ids"
                                   )
    po_line_ids = fields.One2many('outsource.purchase.order.line',
                                  'po_id',
                                  compute="_compute_o2m_all_po_line_ids",
                                  )
    po_line_detail_ids = fields.One2many('outsource.purchase.order.line.detail',
                                             'po_line_id',
                                             compute="_compute_o2m_all_po_line_detail_ids",
                                             )
    @api.depends('approval_ids', 'po_ids')
    def _compute_o2m_all_approval_ids(self):
        self.approval_ids = self.mapped('po_ids.approval_ids')

    @api.depends('po_line_ids', 'po_ids')
    def _compute_o2m_all_po_line_ids(self):
        self.po_line_ids = self.mapped('po_ids.po_line_ids')

    @api.depends('po_line_detail_ids', 'po_ids')
    def _compute_o2m_all_po_line_detail_ids(self):
        self.po_line_detail_ids = self.mapped('po_ids.all_po_line_detail_ids')


    # BUTTON ACTIONS / TRANSITIONS
    # ----------------------------------------------------------
    @api.one
    def set2close(self):
        import ipdb;        ipdb.set_trace()