# -*- coding: utf-8 -*-

from odoo import models, fields
from .utils import choices_tuple


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
    contractor_id = fields.Many2one('res.partner', string='Contractor')