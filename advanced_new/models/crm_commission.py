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
    commission_rewarded = fields.Integer(string='Commission')






