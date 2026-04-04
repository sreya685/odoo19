from odoo import api,fields,models
from odoo.addons.test_convert.tests.test_env import record


class ProductPriceWizard(models.TransientModel):
    _name = 'product.price.wizard'

    new_price = fields.Float(string='New Price')
    product_product_ids = fields.Many2many('product.product',string='Products')
    product_same_price_ids = fields.Many2many('product.product',compute='_compute_product_same_price')
    product_vendors_ids = fields.Many2many('res.partner',compute='_compute_product_vendors_ids')

    def _compute_product_same_price(self):
         for record in self:
             active_id = self.env.context.get('active_id')
             product = self.env['product.product'].browse(active_id)
             products = self.env['product.product'].search([
                 ('list_price','=',product.list_price),
                 ('id','!=',product)
             ])
             print(products)
             record.product_same_price_ids = products

    def _compute_product_vendors_ids(self):
        for record in self:
            active_id = self.env.context.get('active_id')
            product = self.env['product.product'].browse(active_id)
            ven=[]
            vendors = product.mapped('seller_ids')
            for i in vendors:
                    ven.append(i.mapped('partner_id.name'))
            print(ven)
            print(vendors)
            record.product_vendors_ids = ven
            print(record.product_vendors_ids)






    def button_confirm(self):
        for record in self:
            for product in record.product_product_ids:
                product.list_price = record.new_price

            products = self.env['product.product'].search([])
            prd=products.mapped('name')
            print('products are :',prd)


            for i in products:
               if i.filtered(lambda p: p.list_price > 1000):
                      print('product with sales price above 1000 :  ',i.name)

