# -*- coding: utf-8 -*-
from .utils import choices_tuple
from openerp import models, fields, api


class Contractor(models.Model):
    _name = 'outsource.contractor'
    _inherit = 'res.partner'

    CONTRACTORS = choices_tuple(['tamdeed', 'reach', 'inteltec', 'star', 'al hadeer',
                                'skylog', 'telephony', 'sgem', 'xad', 'canal', 'tasc',
                                'innovation', 'penta', 'al rostamani', 'technologia', 'shahid'])

    alias = fields.Char(string="Alias")

    # RELATIONSHIPS
    # ----------------------------------------------------------
    unit_rate_ids = fields.One2many('outsource.unit.rate',
                                  'contractor_id',
                                  string="Unit Rate")

class UnitRate(models.Model):
    _name = 'outsource.unit.rate'
    _rec_name = 'position'
    _description = 'Unit Rate'

    POSITIONS = choices_tuple(['labor', 'driver', 'technician', 'rigger', 'associate engineer',
                               'engineer', 'senior engineer', 'expert engineer', 'car'])

    # BASIC FIELDS
    # ----------------------------------------------------------
    position = fields.Selection(string='Position', selection=POSITIONS)
    level_1 = fields.Float(string='Level 1', digits=(32, 2), default=0.00)
    level_2 = fields.Float(string='Level 2', digits=(32, 2), default=0.00)
    level_3 = fields.Float(string='Level 3', digits=(32, 2), default=0.00)
    level_4 = fields.Float(string='Level 4', digits=(32, 2), default=0.00)
    percent = fields.Float(string='Percent', digits=(32, 2), default=0.00)

    # RELATIONSHIPS
    # ----------------------------------------------------------
    contractor_id = fields.Many2one('outsource.contractor', string='Contractor')
