# -*- coding: utf-8 -*-
from odoo import api,fields,models


class Members(models.Model):
    _name = 'members'
    _description = 'Members'
    _rec_name = 'member_id'


    member_id = fields.Many2one('res.partner',string ='Member')
    maximum_book = fields.Integer(string='Maximum No of checkouts',default=lambda self: self.env['ir.config_parameter'].sudo().get_param('library.borrow_limit') ,store=True)
    check_ids = fields.One2many('checkouts','borrower_id')
    checkout_count = fields.Integer(compute='_compute_checkout_count',string= 'checkout count')
    total_late_returns = fields.Integer(compute='_compute_late_returns',store=True)
    total_penalties = fields.Integer(compute='_compute_total_penalities',store=True)
    maximum_books_in_single_checkout = fields.Integer(string='maximum books in single checkout',default=lambda self: self.env['ir.config_parameter'].sudo().get_param('library.maximum_books') ,store=True)



    @api.depends('check_ids.penalties','check_ids.late_status')
    def _compute_total_penalities(self):
        for record in self:
            t=0
            for rec in record.check_ids:
                if rec.late_status == 'late':
                   t += rec.penalties
            record.total_penalties = t



    @api.depends('total_late_returns')
    def _compute_late_returns(self):
        for record in self:
            record.total_late_returns = self.env['checkouts'].search_count([
                ('borrower_id', '=', record.id),
                ('late_status', '=', 'late')
            ])



    @api.depends('check_ids')
    def _compute_checkout_count(self):
        for record in self:
            record.checkout_count = self.env['checkouts'].search_count([
                ('borrower_id','=',record.id)
            ])



    def action_total_penalties_view(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name':'total penalties',
            'res_model':'checkouts',
            'view_mode':'list,form',
            'domain': [('borrower_id','=',self.id),('late_status','=','late')]

        }

    def action_late_return_view(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name':'late_return',
            'res_model':'checkouts',
            'view_mode':'list,form',
            'domain': [('borrower_id','=',self.id),('late_status','=','late')]

        }


    def action_checkouts_view(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Checkouts',
            'res_model': 'checkouts',
            'view_mode': 'list,form',
            'domain': [('borrower_id', '=', self.id)]

        }


