# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    maximum_no_of_days = fields.Integer(string="Maximum no of Borrowing Days",default=30,config_parameter='library.maximum_no_of_days')
    remainder_days = fields.Integer(string='Remainder days before a book is due',default=10,config_parameter='library.remainder_days')
    penalty_per_hour = fields.Integer(string='Penalty charged for each hour',default=20,config_parameter='library.penalty_per_hour')
    maximum_books = fields.Integer(string='Maximum number of a person can borrow',default=1,config_parameter='library.maximum_books')
    borrow_limit = fields.Integer(string='Maximum Borrowing Limit',default=50,config_parameter='library.borrow_limit')
    late_returns_maximum = fields.Integer(string='Maximum Late returns',default=5,config_parameter='library.late_returns_maximum')