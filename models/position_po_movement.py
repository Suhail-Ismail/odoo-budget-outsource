# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PositionPoMovement(models.Model):
    # TODO BRAINSTORM HOW TO MAKE HISTORY RECORD OF THE MOVEMENT
    _name = 'budget.outsource.position.po.movement'
    _description = 'Position PO Movement'

    # BASIC FIELDS
    # ----------------------------------------------------------

    # RELATIONSHIPS
    # ----------------------------------------------------------
    po_id = fields.Many2one('budget.purchase.order', string='Purchase Order')
    position_id = fields.Many2one('budget.outsource.position', string='Position')

    # COMPUTE FIELDS
    # ----------------------------------------------------------
