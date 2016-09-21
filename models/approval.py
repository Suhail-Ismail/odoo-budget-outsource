# -*- coding: utf-8 -*-
from openerp.exceptions import ValidationError
from .utils import choices_tuple
from openerp import models, fields, api


class Approval(models.Model):
    _name = 'outsource.approval'
    _rec_name = 'ref'
    _description = 'Section Reference'
    _inherit = ['mail.thread']
#    _order = 'po_date desc, po_num'

    # CHOICES
    # ----------------------------------------------------------
    BUDGET_TYPES = choices_tuple(['capex', 'opex', 'revenue'])
    CONTRACTORS = choices_tuple(['tamdeed', 'reach', 'inteltec', 'star', 'al hadeer',
                                'skylog', 'telephony', 'sgem', 'xad', 'canal', 'tasc',
                                'innovation', 'penta', 'al rostamani', 'technologia'])
    STATES = choices_tuple(['waiting purchase order', 'received purchase order'], is_sorted=False)

    # BASIC FIELDS
    # ----------------------------------------------------------
    state = fields.Selection(STATES, default='waiting purchase order')

    ref = fields.Char(string='Section Reference', required=False)
    section = fields.Char(string='Section', required=False)
    service_description = fields.Char(string='Service Description', required=False)
    job_id = fields.Char(string='Job ID', required=False)
    remarks = fields.Text(string='Remarks')
    budget_type = fields.Selection(BUDGET_TYPES)
    contractor = fields.Selection(CONTRACTORS)
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
    required_team_ids = fields.One2many('outsource.required.team',
                                  'approval_id',
                                  string="Required Team")

    # MISC FIELDS
    # ----------------------------------------------------------
    po_temp = fields.Char(string='New Purchase Order', required=False)
    is_linked_to_po = fields.Boolean(string="Is Linked to PO", default=False)

    # CONSTRAINS
    # ----------------------------------------------------------
    # @api.one
    # @api.constrains('state')
    # def _check_description(self):
    #     if self.state == 'received purchase order':
    #         raise ValidationError("Edit is not allowed when PO arrived")

    @api.one
    def create_po_line_details(self):
        if self.state == 'waiting purchase order':
            self.state = 'received purchase order'
            # Create Purchase Order
            # po = self.env['outsource.purchase.order']

            po = self.env['outsource.purchase.order'].create({'po_num': self.po_temp,
                                    'contractor': self.contractor,
                                    'task_num': 'TEST',
                                    'renew_status': 'TEST',
                                    'renew_po_no': 'TEST',
                                    'status': 'TEST',
                                    'type': 'TEST',
                                    'approval_ids': [(4, self.id)],
                                    'po_line_ids': [(0, 0, {
                                        'line_num': '1',
                                        'line_status': 'active'
                                    })],
                                    })
            if po:
                self.is_linked_to_po = True

        # Creates PO Line Details if state is received PO
            write_list = []
            import ipdb; ipdb.set_trace()
            for required_team in self.required_team_ids:
                for level in ['level_1', 'level_2', 'level_3', 'level_4']:
                    quantity_per_level = getattr(required_team, level)
                    for i in range(0, quantity_per_level):
                        write_list.append(
                            (0,0,{
                            'po_os_ref': self.job_id,
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
            self.po_id.po_line_ids[0].write({
                'po_line_detail_ids': write_list
            })


class RequiredTeam(models.Model):
    _name = 'outsource.required.team'
    _rec_name = 'position'
    _description = 'Required Team'

    # CHOICES
    POSITIONS = choices_tuple(['labor', 'driver', 'technician', 'rigger', 'associate engineer',
                               'engineer', 'senior engineer', 'expert engineer', 'car'])

    # RELATIONSHIPS
    # ----------------------------------------------------------
    approval_id = fields.Many2one('outsource.approval', string='Approval')
    position = fields.Selection(POSITIONS)
    level_1 = fields.Integer(string='Level 1', default=0)
    level_2 = fields.Integer(string='Level 2', default=0)
    level_3 = fields.Integer(string='Level 3', default=0)
    level_4 = fields.Integer(string='Level 4', default=0)
