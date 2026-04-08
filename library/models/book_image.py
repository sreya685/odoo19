from odoo import fields,models


class BookImage(models.Model):
    _name = 'book.image'
    _description = 'Book Image'


    images = fields.Many2one('books')