# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Mobilize(models.Model):
    _name = 'budget.outsource.mobilize'
    _rec_name = 'related_position_os_ref'
    _description = 'Mobilize Resource'

    # BASIC FIELDS
    # ----------------------------------------------------------

    active = fields.Boolean()

    # RELATED FIELD
    # ----------------------------------------------------------
    related_position_name = fields.Char(related='position_id.name')
    related_position_os_ref = fields.Char(related='position_id.os_ref')
    related_position_level = fields.Char(related='position_id.level')
    related_position_unit_rate = fields.Monetary(related='position_id.unit_rate', currency_field='currency_id')
    related_position_rate = fields.Monetary(related='position_id.rate', currency_field='currency_id')
    related_position_rate_diff_percent = fields.Monetary(related='position_id.rate_diff_percent', currency_field='currency_id')
    related_position_currency_id = fields.Many2one(related='position_id.currency_id')
    related_position_capex_percent = fields.Integer(related='position_id.capex_percent')
    related_position_opex_percent = fields.Integer(related='position_id.opex_percent')
    related_position_revenue_percent = fields.Integer(related='position_id.revenue_percent')
    related_purchase_order = fields.Char(related='position_id.po_id.no')

    related_resource_name = fields.Char(related='resource_id.name')
    related_resource_type = fields.Char(related='resource_id.type')
    related_resource_type_class = fields.Char(related='resource_id.type_class')
    related_resource_agency_ref_num = fields.Char(related='resource_id.agency_ref_num')
    related_resource_emp_num = fields.Char(related='resource_id.emp_num')
    related_resource_date_of_join = fields.Date(related='resource_id.date_of_join')
    related_resource_has_tool_or_uniform = fields.Boolean(related='resource_id.has_tool_or_uniform')

    related_resource_division = fields.Char(related='resource_id.division_id.name')
    related_resource_section = fields.Char(related='resource_id.section_id.name')
    related_resource_sub_section = fields.Char(related='resource_id.sub_section_id.name')

    # TODO DETERMINE IF IT SHOULD BE HERE
    # director_name = fields.Char()
    #
    # approval_ref_num = fields.Char()
    # approval_reason = fields.Text(blank=True)

    # RELATIONSHIPS
    # ----------------------------------------------------------
    resource_id = fields.Many2one('budget.outsource.resource')
    position_id = fields.Many2one('budget.outsource.position')
