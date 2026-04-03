from odoo import api,fields,models
from odoo.addons.test_convert.tests.test_env import record


class ProductPriceWizard(models.TransientModel):
    _name = 'product.price.wizard'

    new_price = fields.Float(string='New Price')
    product_product_ids = fields.Many2many('product.product',string='Products')
    product_same_price_ids = fields.Many2many(compute='_compute_product_same_price')
    product_vendors_ids = fields.Many2many(compute='_compute_ product_vendors_ids')



    def confirm_button(self):
        self.ensure_one()
        for record in self:
            for product in record.product_product_ids:
                product.list_price = record.new_price


            prd=record.mapped('name')
            for i in prd:
               print(i)
               i.filtered(lambda p: p.list_price > 1000)

