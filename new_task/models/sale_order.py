from email.policy import default

from odoo import  api,fields,models,_
from odoo.addons.test_convert.tests.test_env import record
from odoo.exceptions import UserError
from odoo.orm.decorators import readonly


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Sales Order'

    delivery_remark = fields.Text(string='Delivery Remark')
    is_urgent_delivery = fields.Boolean(string='is urgent')
    preferred_delivery_time = fields.Selection(
        selection=[('morning','Morning'),('afternoon','Afternoon'),('evening','Evening')],
        draft = 'morning',
        string= 'Delivery Time'

    )
    discount_approved = fields.Boolean(default=False)
    discount_approved_by = fields.Many2one('res.users',readonly=True)



    def button_dis_approved(self):
        for record in self:
          c=0
          if record.order_line :
            for line in record.order_line:

                  if line.discount:
                       c += 1
            if c < 1 :
                       raise UserError('at least one order line should have discount')
          else:
              raise UserError('at least one order line should have discount')


        record.discount_approved = True
        record.discount_approved_by = self.env['res.users'].search([('active', '=', True)])

        record.message_post(
            body=_(f"Discount approved by {record.discount_approved_by.name}."),
            message_type="comment",
            subtype_xmlid="mail.mt_comment"
        )




