# -*- coding: utf-8 -*-
from openerp.exceptions import ValidationError
from .utils import choices_tuple
from openerp import models, fields, api


class Approval(models.Model):
    _name = 'outsource.approval'
    _rec_name = 'ref'
    _description = 'Section Reference'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
#    _order = 'po_date desc, po_num'

    # CHOICES
    # ----------------------------------------------------------
    BUDGET_TYPES = choices_tuple(['capex', 'opex', 'revenue'])
    STATES = choices_tuple(['waiting purchase order', 'received purchase order'], is_sorted=False)
    OBJECTIVES = [(1, "For New PO"), (2, "For Renewal"), (3, "For Addendum")]

    # BASIC FIELDS
    # ----------------------------------------------------------
    state = fields.Selection(STATES, default='waiting purchase order')

    ref = fields.Char(string='Section Reference', required=False)
    section = fields.Char(string='Section', required=False)
    service_description = fields.Char(string='Service Description', required=False)
    job_id = fields.Char(string='Job ID', required=False)
    remarks = fields.Text(string='Remarks')
    budget_type = fields.Selection(BUDGET_TYPES)
    budget_team_head = fields.Char(string='TBPC Head', required=False)
    budget_team_sign_date = fields.Date(string='Sign Date')
    budget_team_remarks = fields.Text()

    # REQUESTED BY
    section_head = fields.Char(string='Section Head', required=False)
    request_sign_date = fields.Date(string='Sign Date')

    # END USER APPROVAL
    division_head = fields.Char(string='Division Head', required=False)
    approve_sign_date = fields.Date(string='Sign Date')

    # RELATIONSHIPS
    # ----------------------------------------------------------
    po_id = fields.Many2one('outsource.purchase.order', string='Purchase Order')
    contractor_id = fields.Many2one('outsource.contractor', string='Contractor')

    required_team_ids = fields.One2many('outsource.required.team',
                                  'approval_id',
                                  string="Required Team")

    # MISC FIELDS
    # ----------------------------------------------------------
    po_temp = fields.Char(string='New Purchase Order', required=False)
    objective = fields.Selection(string='Objective', selection=OBJECTIVES)

    def generate_required_details(self):
        # Creates PO Line Details if state is received PO
        detail_list = []
        for required_team in self.required_team_ids:
            for level in ['level_1', 'level_2', 'level_3', 'level_4']:
                quantity_per_level = getattr(required_team, level)
                for i in range(0, quantity_per_level):
                    detail_list.append(
                        (0, 0, {
                            'job_id': self.job_id,
                            'position': required_team.position,
                            'level': ' '.join(level.split('_')),
                            'division': '',
                            'section': self.section,
                            'sub_section': '',
                            'director_name': self.section_head,
                            'frozen_status': '',
                            'approval_ref_num': '',
                            'kpi_2016': '',
                        })
                    )
        return detail_list

    @api.one
    def validate_approval(self):
        """
            Validates Approval
        """
        if not self.po_temp and not self.po_id:
            raise ValidationError("Purchase Order can't be empty")

        if self.state == 'received purchase order':
            raise ValidationError('Purchase Order already Created')

        if self.objective == 1: # For New PO Working
            self.create_po_related_objects()

        elif self.objective == 2: # For Renewal Working
            self.renew_po_related_objects()

        elif self.objective == 3: # For Addendum
            self.update_po_related_objects()

    @api.one
    def create_po_related_objects(self):
        """
        1. PURCHASE ORDER
        Create
        Purchase Order
        Purchase Order Line
        Purchase Order Line Details
        Purchase Order Collection
        """
        detail_list = self.generate_required_details()
        po = self.env['outsource.purchase.order'].create({
                                'po_num': self.po_temp,
                                'contractor_id': self.contractor_id.id,
                                'task_num': 'TEST',
                                'status': 'TEST',
                                'type': 'TEST',
                                'approval_ids': [(4, self.id)],
                                'po_line_ids': [(0, 0, {
                                    'line_num': '1',
                                    'line_status': 'active',
                                    'po_line_detail_ids': detail_list
                                })],
        })
        self.state = 'received purchase order'
        self.env['outsource.purchase.order.collection'].create({'po_ids' : [(4, po.id)]})

    @api.one
    def renew_po_related_objects(self):
        """
        2. RENEW PURCHASE ORDER
        Create
        Purchase Order
        Purchase Order Line
        Purchase Order Line Details
        Purchase Order Collection
        """
        # Reference PO
        # existing po_id must be removed to avoid singleton error
        # the reason might is that it is one2many
        renewed_po = self.po_id
        self.po_id = None

        detail_list = self.generate_required_details()
        po = self.po_id.create({
                                'po_num': self.po_temp,
                                'contractor_id': self.contractor_id.id,
                                'task_num': 'TEST',
                                'status': 'TEST',
                                'type': 'TEST',
                                'po_line_ids': [(0, 0, {
                                    'line_num': '1',
                                    'line_status': 'active',
                                    'po_line_detail_ids': detail_list
                                })],
        })

        po.write({
            'approval_ids': [(4, self.id)],
            'new_po_id': renewed_po.id,
        })
        renewed_po.po_collection_id.write({
            'po_ids': [(4, po.id)]
        })
        self.state = 'received purchase order'

    @api.one
    def update_po_related_objects(self):
        """
        3. Addendum Purchase Order
        Update
        Purchase Order
        Purchase Order Line
        Purchase Order Line Details
        Purchase Order Collection
        """
        detail_list = self.generate_required_details()
        self.po_id.write({
            'po_line_ids': [(0, 0, {
                'line_num': '%s' % (int(self.po_id.po_line_ids.mapped('line_num')[-1]) + 1),
                'line_status': 'active',
                'po_line_detail_ids': detail_list
            })],
        })

        self.state = 'received purchase order'

    # CONSTRAINS
    # ----------------------------------------------------------
    # @api.one
    # @api.constrains('state')
    # def _check_description(self):
    #     if self.state == 'received purchase order':
    #         raise ValidationError("Edit is not allowed when PO arrived")


class RequiredTeam(models.Model):
    _name = 'outsource.required.team'
    _rec_name = 'position'
    _description = 'Required Team'

    # CHOICES
    POSITIONS = choices_tuple(['labor', 'driver', 'technician', 'rigger', 'associate engineer',
                               'engineer', 'senior engineer', 'expert engineer', 'car'])

    # BASIC FIELDS
    # ----------------------------------------------------------
    position = fields.Selection(POSITIONS)
    level_1 = fields.Integer(string='Level 1', default=0)
    level_2 = fields.Integer(string='Level 2', default=0)
    level_3 = fields.Integer(string='Level 3', default=0)
    level_4 = fields.Integer(string='Level 4', default=0)

    # RELATIONSHIPS
    # ----------------------------------------------------------
    approval_id = fields.Many2one('outsource.approval', string='Approval')

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    total_cost = fields.Integer(compute='_compute_total_cost')


    @api.depends('approval_id', 'position', 'level_1', 'level_2', 'level_3', 'level_4', 'total_cost')
    def _compute_total_cost(self):
        for i in ['1', '2', '3', '4']:
            unit_rate = self.approval_id.\
                contractor_id.\
                unit_rate_ids.\
                filtered(lambda rec: rec.position == self.position)
            self.total_cost += getattr(self,'level_' + i) * getattr(unit_rate,'level_' + i)
