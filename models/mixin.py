# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

from odoo.exceptions import ValidationError

class PartnerMixin(models.AbstractModel):
    _name = 'outsource.accessdb.mixin'
    _description = "Access DB Mixin"

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------
    access_db_id = fields.Integer()

    # RELATIONSHIPS
    # ----------------------------------------------------------

    # RELATED FIELDS
    # ----------------------------------------------------------

    # ONCHANGE FIELDS
    # ----------------------------------------------------------

    # CONSTRAINS
    # ----------------------------------------------------------

    # POLYMORPH FUNCTIONS
    # ----------------------------------------------------------
