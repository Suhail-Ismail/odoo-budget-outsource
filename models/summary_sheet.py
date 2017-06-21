# -*- coding: utf-8 -*-
from odoo import models, fields, api

from odoo.exceptions import ValidationError
from ..creator import SBH, DATASHEET
from ..creator.utils import get_distinct_selection


class SummarySheet(models.Model):
    _name = 'outsource.summary.sheet'
    _description = 'Summary Sheet'
    _inherit = ['outsource.accessdb.mixin']

    # CHOICES
    # ----------------------------------------------------------
    GENERATOR_CHOICES = [
        (1, 'SBH for ALL PO NUMBER'),
        (2, 'SBH per PO NUMBER'),
        (3, 'SBH per CONTRACTOR'),
        (4, 'SBH per DIVISION'),
        (5, 'DATASHEET for ALL CONTRACTOR'),
        (6, 'DATASHEET per CONTRACTOR'),
    ]

    # BASIC FIELDS
    # ----------------------------------------------------------
    generator_choice = fields.Selection(selection=GENERATOR_CHOICES)

    po_id = fields.Many2one('outsource.purchase.order', string='Purchase Order')
    contractor = fields.Selection(
        selection=lambda self: get_distinct_selection(self, 'outsource.resource', 'contractor'))
    division = fields.Selection(selection=lambda self: get_distinct_selection(self, 'outsource.resource', 'division'))
    total_required_hours = fields.Integer()
    period_start = fields.Date()
    period_end = fields.Date()
    ramadan_start = fields.Date()
    ramadan_end = fields.Date()

    # BUTTONS
    # ----------------------------------------------------------
    @api.one
    def generate_summary_sheet(self):
        period_start = fields.Date.from_string(self.period_start)
        period_end = fields.Date.from_string(self.period_end)
        ramadan_start = fields.Date.from_string(self.ramadan_start)
        ramadan_end = fields.Date.from_string(self.ramadan_end)
        total_required_hours = fields.Date.from_string(self.total_required_hours)

        if self.generator_choice in [1, 2, 3, 4]:
            obj = SBH(env=self.env, form_name="SBH-FORM.xlsx", xlsx_pass='tbpc19')

        elif self.generator_choice in [5, 6]:
            obj = DATASHEET(env=self.env, form_name="DATASHEET.xlsx", xlsx_pass='tbpc19')

        else:
            raise ValidationError('Invalid Choice')

        if self.generator_choice == 1:
            obj.make_sbh_per_contractor('all', period_start, period_end, ramadan_start, ramadan_end,
                                        total_required_hours)

        elif self.generator_choice == 2:
            obj.make_sbh_per_po(self.po_id.po_num, period_start, period_end, ramadan_start, ramadan_end,
                                total_required_hours)

        elif self.generator_choice == 3:
            obj.make_sbh_per_contractor(self.contractor, period_start, period_end, ramadan_start, ramadan_end,
                                        total_required_hours)

        elif self.generator_choice == 4:
            obj.make_sbh_per_division(self.po_id.po_num, self.division, period_start, period_end, ramadan_start,
                                      ramadan_end, total_required_hours)

        elif self.generator_choice == 5:
            obj.make_datasheet_per_contractor('all', period_start, period_end, ramadan_start, ramadan_end,
                                              total_required_hours)

        elif self.generator_choice == 6:
            obj.make_datasheet_per_contractor(self.contractor, period_start, period_end, ramadan_start, ramadan_end,
                                              total_required_hours)

        zip_path = obj.make_zip()

        obj.attach(self.env, self.id, self._name, zip_path)
        obj.cleanup()
