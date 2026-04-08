# -*- coding: utf-8 -*-
from email.policy import default

from odoo import api,fields,models,_



class Books(models.Model):
    _name = 'books'
    _description = 'Library Books'
    _rec_name='book_name'

    book_name = fields.Text(string='Title',required=True)
    description = fields.Text(string='Description')
    isbn = fields.Char(string='ISBN',default=lambda self: _('New'))
    price = fields.Float(string='Price')
    cost = fields.Float(string='Cost')
    status = fields.Selection(
        string='Status',
        selection=[('available','Available'),('unavailable','Unavailable'),('coming soon','Coming Soon')],default='available')
    authors_id = fields.Many2one('authors',string='Authors')
    publishers_id = fields.Many2one('publishers',string='Publishers')
    genres_id = fields.Many2one('genres',string='Genres')
    tag_ids = fields.Many2many('tags',string='Tags')
    publication_year_id = fields.Integer(related='publishers_id.publication_year',string='Publication Year')
    prd_id = fields.Many2one('product.product')
    image_1920 = fields.Image(string='Image',optional=True)
    language = fields.Char(string='language')
    condition = fields.Selection(
        string = 'condition',
        selection= [('new','New'),('used','Used')],
        default='new'
    )
    user_id = fields.Many2one('res.users',default=lambda self: self.env.user)
    user_name = fields.Char(related='user_id.name')
    book_image = fields.One2many('book.image','images')

     # to create sequence to isbn
    def create(self,vals):

         if vals.get('isbn',_('New')) == _('New'):
               vals['isbn']=self.env['ir.sequence'].next_by_code('books') or _('New')
         n = vals.get('book_name')
         p = vals.get('price')
         c = vals.get('cost')
         x=self.env['product.product'].create({
             'name': n,
             'list_price': p,
             'type' : 'service',
             'standard_price': c
         })
         vals['prd_id'] = x.id
         return super().create(vals)


    # to create available button
    def available_book(self):
      for record in self:
        if record.book_name and record.isbn:
            record.status = 'available'



    # to create unavailable button
    def unavailable_book(self):
        for record in self:
            record.status = 'unavailable'



    # to create coming soon button
    def coming_book(self):
        for record in self:
            record.status = 'coming soon'



    borrow_count = fields.Integer(compute='_compute_borrow_count',string='Borrow Count',store=True)
    @api.depends()
    def _compute_borrow_count(self):
        for record in self:
            record.borrow_count = self.env['checkouts'].search_count([
                ('book_id', '=', record.id),
                ('status', '=', 'available')
            ])
