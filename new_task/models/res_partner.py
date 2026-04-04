from email.policy import default

from odoo import api,fields,models




class ResPartner(models.Model):
    _inherit = 'res.partner'

    most_sold_product = fields.Many2one('product.product')
    total_sold_quantity = fields.Integer(compute='_compute_total_sold_quantity',default=0)
    minimum_sales_price = fields.Integer(compute='_compute_total_sold_quantity',default=0)
    maximum_sales_price = fields.Integer(compute='_compute_total_sold_quantity',default=0)






    @api.depends('most_sold_product')
    def _compute_total_sold_quantity(self):
        for record in self:
          if record:
            order=self.env['sale.order.line'].search([
                ('order_partner_id','=',record.id)]
            )

            if record.most_sold_product:

                        qty = 0
                        for i in order:
                           qty += i.product_uom_qty
                        record.total_sold_quantity = qty
                        orde = self.env['sale.order.line'].search([
                            ('product_template_id', '=', record.most_sold_product)
                        ])
                        amt=[]
                        for line in orde:
                                amt.append(line.price_subtotal)

                        mini = min(amt)
                        record.minimum_sales_price = mini
                        maxi= max(amt)
                        record.maximum_sales_price = maxi

            else:
                record.total_sold_quantity = 0
                record.minimum_sales_price = 0
                record.maximum_sales_price = 0

    def sale_order_count_view(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'sale orders',
            'res_model': 'sale.order',
            'view_mode': 'list,form',
            'domain': [('partner_id', '=', self.id)]

        }