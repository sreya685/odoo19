from odoo import fields,models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    restricted_tags = fields.Char(
        "restricted_tags",
        default=lambda self: self.env['ir.config_parameter'].get_param('task_new.restricted_customer_tag'))

    def action_confirm(self):


        # if self.amount_residual:
        #    total_due = self.amount_residual
        credit_limit = self.env['ir.config_parameter'].sudo().get_param('task_new.credit_limit_threshold')
        print(self.restricted_tags)
        print(credit_limit)
        customer_restrict_tags = self.partner_id.category_id.name
        # for record in self:
        #  for i in record.restricted_tags:
        #    if customer_restrict_tags == i.name :
        #        # if total_due > credit_limit:
        #           raise ValidationError('blocked from changing into sale order')
        #
        #    else:
        #          super().action_confirm()






