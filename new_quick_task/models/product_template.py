from email.policy import default

from odoo import fields,models,api,_
from odoo.exceptions import ValidationError
from datetime import date

from dateutil.relativedelta import relativedelta



class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template'



    # calculate_avg = fields.Float(compute='_compute_avg',default=0.0,string='Average')
    last_price_update = fields.Date(string='last price update',default=date.today())
    # @api.constrains('list_price')
    def write(self,vals):
        for record in self:
                    if 'list_price' in vals:
                        print('rec',record)
                        new_price = vals.get('list_price')
                        print('new_price',new_price)
                        today = date.today()
                        calculate_time = today - relativedelta(months=+1)


                        prd = record.name
                        print('prd',prd)
                        y=self.env['sale.order.line'].search([
                            # ('product_id','=',record.id),
                            ('order_id.state','=','sale'),
                            ('order_id.date_order','>=',calculate_time)
                        ])
                        print('-------------',y)


                # lines=[]
                # for line in y.order_line:
                #     lines.append(line.price_unit)
                        prices = y.mapped('price_unit')

                        print('prices:',prices)
                        if len(prices) != 0 :
                            calculate_avg = sum(prices)/len(prices)

                            if new_price:
                               if new_price < (calculate_avg) * 0.08:
                                 if not self.env.user.has_group('sales_team.group_sale_manager'):
                                               raise ValidationError('new price is less than 80%')


                            print('average :',calculate_avg)
                    r =   super(ProductTemplate, self).write(vals)
                    today = date.today()
                    if 'list_price' in vals:
                        # record.last_price_update = today
                        record.product_variant_ids.write({
                            'last_price_update': today



                        } )
                    return r
