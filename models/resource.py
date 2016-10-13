# -*- coding: utf-8 -*-
from .utils import choices_tuple
from openerp import models, fields, api

class Resource(models.Model):
    _inherit = 'res.partner'
    _rec_name = 'name'
    _description = 'Resource'

    # CHOICES
    # ----------------------------------------------------------
    STATES = choices_tuple(['active', 'closed'], is_sorted=False)

    # BASIC FIELDS
    # ----------------------------------------------------------
    is_outsource_resource = fields.Boolean(string='is Outsource Resource')

    state = fields.Selection(string='Status', selection=STATES, default='active')
    type = fields.Char(string='Type')
    type_class = fields.Char(string='Type Class')
    agency_ref_num = fields.Char(string='Agency Reference')
    emp_num = fields.Char(string='Employee Number')
    date_of_join = fields.Date(string='Date of Join')
    remarks = fields.Text()
    has_tool_or_uniform = fields.Boolean(string='has tool or uniform')

    # RELATIONSHIPS
    # ----------------------------------------------------------
    po_line_detail_id = fields.Many2one('outsource.purchase.order.line.detail', string='Line Detail')
    contractor_id = fields.Many2one('res.partner', string='Contractor')
    claim_ids = fields.Many2many('outsource.claim',
                                   relation='claim_resource_rel',
                                  string="Claims")
    position_history_ids = fields.One2many('outsource.position.history',
                                           'resource_id',
                                           string="Position Histories")


    # COMPUTE FIELD REFERENCES
    # ----------------------------------------------------------
    _compute_resource_po_id = fields.Many2one('outsource.purchase.order', string='Compute Purchase Order')

class PositionHistory(models.Model):
    _name = 'outsource.position.history'
    _description = 'Position History'

    # CHOICES
    # ----------------------------------------------------------
    STATUSES = choices_tuple(['active', 'closed'], is_sorted=False)

    status = fields.Selection(string='Status', selection=STATUSES, default='active')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

    remarks = fields.Text()

    # RELATIONSHIPS
    # ----------------------------------------------------------
    resource_id = fields.Many2one('res.partner',
                                  string='Employee')

    po_line_detail_id = fields.Many2one(
        'outsource.purchase.order.line.detail',
        string='Purchase Order Line Detail',
    )

    # EXPOSE FIELDS
    # ----------------------------------------------------------
    contractor_id = fields.Many2one('res.partner',
                                    related='resource_id.contractor_id',
                                    string='Contractor')
