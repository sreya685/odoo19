from odoo import api,fields,models




class ProductProduct(models.Model):
    _inherit = 'product.product'


    internal_remarks = fields.Char(string='Internal Remarks')
    discounted_price = fields.Float(compute='_compute_discounted_price',string='Discounted Price')
    price_category = fields.Char(compute='_compute_discounted_price',string='Price Category')


    @api.depends('list_price')
    def _compute_discounted_price(self):
        for record in self:
            if record.list_price :
                record.discounted_price = record.list_price  - (record.list_price)*0.10
                if record.list_price >1000:
                   record.price_category = 'Premium'
                else:
                    record.price_category = 'Standard'
