
from odoo import fields,models,_



class RevenueCommission(models.Model):
    _name = 'revenue.commission'
    _description = 'Revenue Commission'


    # commission = fields.Char(string='Commission ID',default=lambda self: _('New'))
    commission = fields.Char(string='Commission ID')
    from_amount = fields.Integer(string='From Amount')
    to_amount = fields.Integer(string='To Amount')
    rate = fields.Integer(string='Rate (%)')
    commission_id = fields.Many2one('crm.commission')

    # def create(self, vals):
    #     if vals.get('commission', _('New')) == _('New'):
    #         vals['commission'] = self.env['ir.sequence'].next_by_code('revenue.commission') or _('New')
    #     return super().create(vals)