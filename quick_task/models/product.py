from odoo import api,fields,models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    project = fields.Many2one('project.project',store=True)