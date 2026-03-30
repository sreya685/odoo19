from email.policy import default

from odoo import fields,models,api




class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Sales Order'


    commission_amt = fields.Float(compute='compute_commission',string='Commission',default=0.0,store=True)
    @api.depends('team_id.comm_id','user_id.comm_id')
    def compute_commission(self):
        if self.team_id.comm_id or self.user_id.comm_id:
          plan = self.team_id.comm_id
          sales = self.env['sale.order'].search([
              ('state', '=', 'sale')
          ])
          amount = sum(sales.mapped('amount_total'))
          if plan.type == 'revenue_wise':
            if plan.mode == 'straight':

                 for line in plan.commission_mode:
                    if  line.from_amount <= amount <= line.to_amount:
                        self.commission_amt = amount * (line.rate)/100

            if plan.mode == 'graduated':
                 for line in plan.commission_mode:
                     b=0
                     bb=0
                     if amount > line.from_amount:

                          b = min(amount,line.to_amount)
                          if b == amount:
                             b - (line.from_amount)

                          bb = b * (line.rate)/100
                 self.commission_amt = bb



      # 10 20  2    10<150-20=130<=20   40*2%
      # 20 30  3    20<150-130=20<=30  20*3%
