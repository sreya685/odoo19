from odoo import fields,models


class CRMTeam(models.Model):
    _inherit = 'crm.team'



    comm_id = fields.Many2one('crm.commission')