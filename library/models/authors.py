# -*- coding: utf-8 -*-
from odoo import fields,models


class Authors(models.Model):
    _name = 'authors'
    _description = 'Authors'
    _rec_name = 'author_name'

    author_name = fields.Text(string='Author Name')
    description = fields.Text(string="Author's Biography")
    author_book_ids = fields.One2many('books','authors_id')