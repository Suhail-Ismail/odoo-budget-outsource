from odoo import models, api, fields
 
 
class ChangeSpocPasswordWizard(models.TransientModel):
    _inherit = "change.password.wizard"
    _description = "Change Password Wizard"
    
    def _default_user_ids(self):
        res = []
        if self._context.get('active_model') == 'budget.outsource.spoc':
            user_ids = self._context.get('user_ids') or []
            res = [
                (0, 0, {'user_id': user.id, 'user_login': user.login})
                for user in self.env['res.users'].browse(user_ids)
            ]
        else:
            res = super(ChangeSpocPasswordWizard, self)._default_user_ids()
        return res
        
    user_ids = fields.One2many('change.password.user', 'wizard_id', string='Users', default=_default_user_ids) 