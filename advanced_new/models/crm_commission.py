from odoo import fields,models,api

class CRMCommission(models.Model):
    _name = 'crm.commission'
    _description = 'CRM Commission'
    _rec_name = 'commission_name'

    commission_name = fields.Char(string='Commission Name')
    active = fields.Boolean(string='Active',default=True)
    from_date = fields.Date(string='From Date',store=True)
    to_date = fields.Date(string='To Date',store=True)
    type = fields.Selection(
        string='Type',
        selection=[('product_wise','Product Wise'),('revenue_wise','Revenue Wise')],
        default = 'product_wise'

    )
    mode = fields.Selection(
        selection=[('straight', 'Straight'), ('graduated', 'Graduated')],
        default='straight',
        string='Mode'
    )
    commission_mode = fields.One2many('revenue.commission','commission_id')
    sales_team_target = fields.Integer(string='Sales Team')

    @api.onchange('commission_mode')
    def compute_team_target(self):
        sales_t_t = self.env['sale.order'].search_count([
          ('team_id','=','sales')
      ])
        if sales_t_t:
            s = sum(sales_t_t.mapped('amount_total'))
            self.sales_team_target = s




