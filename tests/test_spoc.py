from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
 
class TestSpoc(TransactionCase):
    at_install = False
    post_install = True

    def setUp(self):
        spoc_01 = {
            'name': 'Test',
            'login':"test@test123.com",
            'active':True,  #Spoc is active by default on create
            'division_id': self.division_id.id,
            'section_id': self.section_id.id
        }
        self.spoc_id = self.env['budget.outsource.spoc'].create(spoc_01)
 
    # Check creating spoc
    def test_create(self):
        self.assertTrue(self.spoc_id, "Error creating new spoc")
        
    # Check creating spoc create user
    def test_create_user(self):
        self.assertTrue(self.spoc_id.user_id, "Could not create user for spoc {} with id {}".format(self.spoc_id.name, self.spoc_id.id))
 
    # Check SPOC can be edited
    def test_edit(self):
        division01_id = self.env['budget.enduser.division'].create({'name': 'Division01', 'alias': 'division01'})
        self.spoc_id.write({'division_id': division01_id.id})
        self.assertEqual(self.spoc_id.division_id.id, division01_id.id, "Could not change spoc division from {} to {}".format(self.division_id.name, division01_id.name) )
 
    # Check SPOC can be deleted
    def test_spoc_unlink(self):
        spoc_temp_id = self.spoc_id.id
        self.spoc_id.unlink()
        exist = self.env['budget.outsource.spoc'].search([('id', '=', spoc_temp_id)], limit=1)
        self.assertFalse(exist, "Could not delete spoc with id {}".format(spoc_temp_id))
     
    # Check division can have more than one spoc
    def test_more_spoc1(self):
        spoc_02 = {
            'name': 'Test',
            'login':"test123@test123.com",
            'password':"123",
            'division_id': self.division_id.id,
            'section_id': self.section_id.id
        }
        with self.assertRaises(ValidationError):
            # Creating spoc with same division
            self.env['budget.outsource.spoc'].create(spoc_02)

    # Check division can have more than one spoc
    def test_more_spoc2(self):
        spoc_02 = {
            'name': 'Test',
            'login':"test123@test123.com",
            'division_id': self.division_id.id,
            'section_id': self.section_id.id
        }
        # make first spoc inactive
        self.spoc_id.write({'active':False})
        spoc_02_id = self.env['budget.outsource.spoc'].create(spoc_02)
        with self.assertRaises(ValidationError):
            # making first spoc active from spoc model
            self.spoc_id.write({'active':True})

    # Check division can have more than one spoc
    def test_more_spoc3(self):
        spoc_02 = {
            'name': 'Test',
            'login':"test123@test123.com",
            'division_id': self.division_id.id,
            'section_id': self.section_id.id
        }
        # make first spoc inactive
        self.spoc_id.write({'active':False})
        spoc_02_id = self.env['budget.outsource.spoc'].create(spoc_02)
        with self.assertRaises(ValidationError):
            # making first spoc active from the res_user model
            self.spoc_id.mapped('user_id').write({'active':True}) 