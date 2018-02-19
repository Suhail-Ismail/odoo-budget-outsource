# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Dumper(models.Model):
    _name = 'outsource.dumper'

    # BASIC FIELDS
    # ----------------------------------------------------------

    # RELATIONSHIPS
    # ----------------------------------------------------------

    # METHODS
    # ----------------------------------------------------------
    def clear_all(self):
        tables = [
            'outsource.purchase.order',
            'outsource.purchase.order.line',
            'outsource.purchase.order.line.detail',
            'outsource.resource',
            'outsource.invoice',
            'outsource.unit.rate'
        ]
        for table in tables:
            self.env.cr.execute("TRUNCATE %s CASCADE" % table.replace('.', '_'))
            self.env.cr.commit()

        return True
