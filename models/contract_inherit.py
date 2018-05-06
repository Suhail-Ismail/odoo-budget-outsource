# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.budget_utilities.models.utilities import num_to_shorthand


class Contract(models.Model):
    _inherit = 'budget.contractor.contract'

    is_outsource = fields.Boolean('Is Outsource', default=False)
