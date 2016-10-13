# -*- coding: utf-8 -*-
from .utils import choices_tuple
from openerp import models, fields, api

class Claim(models.Model):
    _name = 'outsource.claim'
    _rec_name = 'claim_num'

    # CHOICES
    # ----------------------------------------------------------
    STATES = choices_tuple(['draft', 'claim line created', 'closed'], is_sorted=False)

    # BASIC FIELDS
    # ----------------------------------------------------------
    state = fields.Selection(STATES, default='draft')

    claim_num = fields.Char(string='Claim Number')
    claim_date = fields.Date(string='Claim Date')

    # RELATIONSHIPS
    # ----------------------------------------------------------
    contractor_id = fields.Many2one('res.partner', string='Contractor')
    po_id = fields.Many2one('outsource.purchase.order', string='Purchase Order')
    period_id = fields.Many2one('outsource.claim.period', string='Period')
    claim_line_ids = fields.One2many('outsource.claim.line',
                                           'claim_id',
                                           string="claim Lines")
    resource_ids = fields.Many2many('res.partner',
                                     relation='claim_resource_rel',
                                        string="Resources")

    # RELATED FIELDS
    # ----------------------------------------------------------
    required_hours = fields.Integer(related='period_id.required_hours', string='Required Hours')

    @api.one
    def set2close(self):
        pass

    @api.one
    def set2created_claim_details(self):
        for resource_id in self.resource_ids:
            self.env['outsource.claim.line'].create({
                'resource_id': resource_id.id,
                'claim_id': self.id,
                'claim_hour': self.required_hours,
                'claim_claim': self.required_hours,
            })

            self.state = 'claim line created'

class claimLine(models.Model):
    _name = 'outsource.claim.line'
    _rec_name = 'resource_id'

    # CHOICES
    # ----------------------------------------------------------
    STATES = choices_tuple(['active', 'closed'], is_sorted=False)

    # BASIC FIELDS
    # ----------------------------------------------------------
    state = fields.Selection(STATES, default='active')

    claim_hour = fields.Float(string='claim Hour', digits=(32, 2), default=0.00)
    claim_claim = fields.Float(string='claim Claim', digits=(32, 2), default=0.00)
    claim_cert_amount = fields.Float(string='Certified Amount', digits=(32, 2), default=0.00)
    remarks = fields.Text()

    # RELATIONSHIPS
    # ----------------------------------------------------------
    resource_id = fields.Many2one('res.partner', string='Resource')
    claim_id = fields.Many2one('outsource.claim', string='claim')


class Period(models.Model):
    _name = 'outsource.claim.period'

    @api.multi
    def name_get(self):
        result = []
        for r in self:
            period = fields.Datetime.from_string(r.period_start)
            new_name = u"%s" % period.strftime("%B - %y")

            result.append((r.id, new_name))
        return result


    # BASIC FIELDS
    # ----------------------------------------------------------
    period_start = fields.Date(string='Period Start', required=True)
    period_end = fields.Date(string='Period End', required=True)
    ramadan_start = fields.Date(string='Ramadan Start')
    ramadan_end = fields.Date(string='Ramadan End')
    remarks = fields.Text(string='Remarks')

    # RELATIONSHIPS
    # ----------------------------------------------------------
    claim_ids = fields.One2many('outsource.claim',
                                  'period_id',
                                  string="claims")

    # COMPUTED FIELDS
    # ----------------------------------------------------------
    required_hours = fields.Integer(compute='_compute_required_hours', store=True)


    @api.one
    @api.depends('period_start', 'period_end', 'ramadan_start', 'ramadan_end')
    def _compute_required_hours(self):

        period_start = fields.Datetime.from_string(self.period_start)
        period_end = fields.Datetime.from_string(self.period_end)
        ramadan_start = fields.Datetime.from_string(self.ramadan_start)
        ramadan_end = fields.Datetime.from_string(self.ramadan_end)

        total_days = (period_end - period_start).days + 1
        ramadan_days = 0
        if ramadan_start and ramadan_end:
            start = period_start
            if period_start < ramadan_start:
                start = ramadan_start
            end = period_end
            if ramadan_end < period_end:
                end = ramadan_end

            ramadan = end - start
            ramadan_days = ramadan.days + 1

        normal_days = total_days - ramadan_days

        # +1 is a corrections factor to count all days within a period
        self.required_hours = round(normal_days * 48 / 7) + round(ramadan_days * 36 / 7)
