from odoo import fields,models





class ResCompany(models.Model):
    _inherit = 'res.company'



    restrict_tags = fields.Many2many('res.partner.category')