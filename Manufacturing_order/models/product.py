from odoo import api,fields,models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_manufacturable = fields.Boolean( string="is manufacturable")