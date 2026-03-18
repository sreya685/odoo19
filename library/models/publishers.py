# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Publishers(models.Model):
    _name = 'publishers'
    _description = 'Library Books Publishers'
    _rec_name = 'publishers_name'

    publishers_name = fields.Text(string='Publisher Name')
    address = fields.Text(string="Address")
    publishers_book_ids = fields.One2many('books','publishers_id')
    publication_year = fields.Integer(string='Publication Year')