# -*- coding: utf-8 -*-
from .utils import choices_tuple
from openerp import models, fields, api

class UnitRate(models.Model):
    _name = 'outsource.unit.rate'
    _rec_name = 'position'
    _description = 'Unit Rate'

    # CHOICES
    # ----------------------------------------------------------
    # contractors is same as Approval Model
    CONTRACTORS = choices_tuple(['tamdeed', 'reach', 'inteltec', 'star', 'al hadeer',
                                'skylog', 'telephony', 'sgem', 'xad', 'canal', 'tasc',
                                'innovation', 'penta', 'al rostamani', 'technologia', 'shahid'])
    # positions is same as RequiredTeam Model
    POSITIONS = choices_tuple(['labor', 'driver', 'technician', 'rigger', 'associate engineer',
                               'engineer', 'senior engineer', 'expert engineer', 'car'])

    # BASIC FIELDS
    # ----------------------------------------------------------
    contractor = fields.Selection(string='Constractor', selection=CONTRACTORS)
    position = fields.Selection(string='Position', selection=POSITIONS)
    level = fields.Integer(string='Level')
    amount = fields.Float(string='Amount', digits=(32, 2), default=0.00)
    percent = fields.Float(string='Percent', digits=(32, 2), default=0.00)