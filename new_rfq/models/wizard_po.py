from odoo import api, fields, models,Command


class Wizard_Po(models.TransientModel):
    _name = 'wizard.po'



    quantity = fields.Integer(string='Quantity')
    price = fields.Float(string='Price')


    def confirm_wizard_button(self):
        active_id = self.env.context.get('active_id')
        # print(active_id)
        product = self.env['product.product'].browse(active_id)
        vendors = product.mapped('seller_ids')

        for vendor in vendors:
            first_vendor= vendor.partner_id.id
            break

        for record in self:
            lines=[]
            lines.append(Command.create({
                'product_id' : product.id,
                'product_qty' : record.quantity,
                'price_unit' : record.price
            }))
            self.env['purchase.order'].create({
                'order_line' : lines,
                'state': 'purchase',
                'partner_id' : first_vendor
            })