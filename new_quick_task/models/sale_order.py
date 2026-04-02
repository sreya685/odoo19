from email.policy import default

from odoo import fields,models,api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta






class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Sales Order'



    calculate_avg = fields.Float(compute='_compute_avg',default=0.0)

    @api.onchange('order_line.price_unit')
    def on_change_list_price(self):
        for record in self:
            print('rec',record)
            calculate_time = record.date_order
            if record.state =='sale':

              if  calculate_time <= record.date_order + relativedelta(months=+1) :


                    for line in record.order_line:
                        prd = line.product_template_id[0]

                    y=self.env['sale.order'].search([
                        ('order_line.product_template_id','=',prd),
                        ('state','=','sale')
                    ])
                    print(y)

    @api.depends('order_line.price_unit')
    def _compute_avg(self):
        for record in self:
            lines=[]
            for line in record.order_line:
                lines.append(line.price_unit)
            s=0
            for i in lines:
                    if  record.calculate_avg == 0:
                        s += i
                        record.calculate_avg = s/len(lines)
                    else:
                        if i < (record.calculate_avg) * 0.08:
                            raise ValidationError('new price is less than 80%')

                        


