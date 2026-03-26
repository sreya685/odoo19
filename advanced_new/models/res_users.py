from odoo import fields,models



class ResUsers(models.Model):
    _inherit ='res.users'



    comm_id = fields.Many2one('crm.commission')
