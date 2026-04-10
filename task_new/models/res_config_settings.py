from email.policy import default

from odoo import fields, models,api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    restricted_customer_tag_ids = fields.Many2many("res.partner.category",related="company_id.restrict_tags",readonly=False)
    credit_limit_threshold = fields.Float(default="500",config_parameter='task_new.credit_limit_threshold',store=True)
    restricted_customer_tag = fields.Char(
        "restricted_customer_tag",config_parameter='task_new.restricted_customer_tag',default=''
        )
    #
    #
    #
    @api.model

    def set_values(self):
        super().set_values()
        self.env['ir.config_parameter'].set_param('task_new.restricted_customer_tag')
    #
    # def get_values(self):
    #     res = super(ResConfigSettings, self).get_values()
    #     res['customer_tags'] = str(self.env['ir.config_parameter'].get_param('task_new.customer_tags'))
    #
    #     return res

