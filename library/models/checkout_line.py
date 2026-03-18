# -*- coding: utf-8 -*-
from odoo import api,fields,models


class CheckoutLine(models.Model):
    _name = 'checkout.line'
    _description = 'Checkout Line'
    _rec_name = 'check_ids'

    check_ids = fields.Many2one('checkouts',string='Checkout line', ondelete="cascade")
    borrowed_book_id  = fields.Many2one('books',string='Books',domain="[('status', '=', 'available')]")
    price = fields.Float(related='borrowed_book_id.price',string='Price')

