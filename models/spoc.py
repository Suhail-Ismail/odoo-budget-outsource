# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Spoc(models.Model):
    _name = 'budget.outsource.spoc'
    _inherit = 'budget.enduser.mixin'
     
    # BASIC FIELDS
    name = fields.Char(string='Name')
 
    login = fields.Char(string='Login')
 
    remark = fields.Char(string='Remarks')
    # END BASIC FIELDS
 
    # RELATIONSHIPS
    user_id = fields.Many2one('res.users', ondelete='restrict')
    # END RELATIONSHIPS
 
    # RELATED FIELDS
    # ----------------------------------------------------------
    active = fields.Boolean(related="user_id.active",
                            store=True, 
                            )
     # END RELATED FIELDS
     
     # CONSTRAINS
    # To make sure only one spoc is active at a time
    @api.one
    @api.constrains('division_id', 'active')
    def _check_one_active_spoc_per_division(self):
        division = self.mapped('division_id').id
        active = self.env['budget.outsource.spoc'].search([('division_id', '=', division)]).filtered('active').mapped('user_id')
        is_current_user_active = self.mapped('active')[0]
        if len(active) > 1 and is_current_user_active:
            raise ValidationError("Division can only have one active spoc.")
     # END CONSTRAINS
 
     # POLYMORPH FUNCTIONS
    @api.model
    def create(self, values):
        user_id = self.env['res.users'].create({'name':values.get('name', False), 'login':values.get('login', False)})
        values['user_id'] = user_id.id
        # User will be active when creating
        values['active'] = True
        return super(Spoc, self).create(values)
 
    @api.multi
    def write(self, values):
        values['name'] = self.name
        if not values.get('login', False):
            values['login'] = self.login
        self.mapped('user_id').write({'name':values['name'], 'login':values['login']})
        return super(Spoc, self).write(values)
 
    @api.multi
    def unlink(self):
        # For deactivating corresponding user when spoc is removed
        self.mapped('user_id').write({'active': False})
        return super(Spoc, self).unlink()
     # END POLYMORPH FUNCTIONS 