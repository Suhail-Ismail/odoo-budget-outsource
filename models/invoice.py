# -*- coding: utf-8 -*-
from .utils import choices_tuple
from openerp import models, fields, api

class Invoice(models.Model):
    _name = 'outsource.invoice'
    _rec_name = 'invoice_num'

    # CHOICES
    # ----------------------------------------------------------
    STATES = choices_tuple(['draft', 'invoice line created', 'closed'], is_sorted=False)

    # BASIC FIELDS
    # ----------------------------------------------------------
    state = fields.Selection(STATES, default='draft')

    invoice_num = fields.Char(string='Invoice Number')
    invoice_date = fields.Date(string='Invoice Date')

    # RELATIONSHIPS
    # ----------------------------------------------------------
    contractor_id = fields.Many2one('res.partner', string='Contractor')
    po_id = fields.Many2one('outsource.purchase.order', string='Purchase Order')
    period_id = fields.Many2one('outsource.invoice.period', string='Period')
    invoice_line_ids = fields.One2many('outsource.invoice.line',
                                           'invoice_id',
                                           string="Invoice Lines")
    resource_ids = fields.Many2many('res.partner',
                                     relation='invoice_resource_rel',
                                        string="Resources")

    # RELATED FIELDS
    # ----------------------------------------------------------
    required_hours = fields.Integer(related='period_id.required_hours', string='Required Hours')

    @api.one
    def set2close(self):
        pass

    @api.one
    def set2created_invoice_details(self):
        for resource_id in self.resource_ids:
            self.env['outsource.invoice.line'].create({
                'resource_id': resource_id.id,
                'invoice_id': self.id,
                'invoice_hour': self.required_hours,
                'invoice_claim': self.required_hours,
            })

            self.state = 'invoice line created'

class InvoiceLine(models.Model):
    _name = 'outsource.invoice.line'
    _rec_name = 'resource_id'

    # CHOICES
    # ----------------------------------------------------------
    STATES = choices_tuple(['active', 'closed'], is_sorted=False)

    # BASIC FIELDS
    # ----------------------------------------------------------
    state = fields.Selection(STATES, default='active')

    invoice_hour = fields.Float(string='Invoice Hour', digits=(32, 2), default=0.00)
    invoice_claim = fields.Float(string='Invoice Claim', digits=(32, 2), default=0.00)
    invoice_cert_amount = fields.Float(string='Certified Amount', digits=(32, 2), default=0.00)
    remarks = fields.Text()

    # RELATIONSHIPS
    # ----------------------------------------------------------
    resource_id = fields.Many2one('res.partner', string='Resource')
    invoice_id = fields.Many2one('outsource.invoice', string='Invoice')


class Period(models.Model):
    _name = 'outsource.invoice.period'

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
    invoice_ids = fields.One2many('outsource.invoice',
                                  'period_id',
                                  string="Invoices")

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
