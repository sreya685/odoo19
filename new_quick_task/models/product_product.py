from odoo import fields,models,api



class ProductProduct(models.Model):
    _inherit = 'product.product'

    last_price_update = fields.Date(string='Last Update Date')


