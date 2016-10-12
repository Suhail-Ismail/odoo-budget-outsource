# -*- coding: utf-8 -*-
from openerp import models, fields, api
from .utils import choices_tuple

# ONGOING DESIGN
class Task(models.Model):
    _name = 'outsource.task'
    _rec_name = 'task_num'
    _description = 'Task'

    task_num = fields.Char(string='Task Number')

    # RELATIONSHIPS
    # ----------------------------------------------------------
    po_id = fields.Many2one('outsource.purchase.order', string='Purchase Order')