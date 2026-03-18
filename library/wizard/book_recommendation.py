# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo import Command
from odoo.exceptions import ValidationError


class BookRecommendation(models.TransientModel):
    _name = 'book.recommendation'
    _description = "Recommendation for Books"
    recommendation_ids = fields.Many2many('books', string='Suggestions',domain="[('status', '=', 'available')]")

    @api.model
    def default_get(self, fields_list):
        results = super().default_get(fields_list)
        active_id = self.env.context.get('active_id')
        checkout = self.env['checkouts'].browse(active_id)
        if not checkout:
            return results
        selected_books = checkout.checkouts_line_ids.mapped('borrowed_book_id')
        authors = selected_books.mapped('authors_id')
        genres = selected_books.mapped('genres_id')


        book_author = self.env['books'].search([
                ('authors_id', 'in', authors.ids),
                ('status', '=', 'available'),
                ('id', 'not in', selected_books.ids),
            ])
        book_genre = self.env['books'].search([
            ('genres_id', 'in', genres.ids),
            ('status', '=', 'available'),
            ('id', 'not in', selected_books.ids)
            ])
        popular_books = self.env['books'].search([
            ('id', 'not in', selected_books.ids),
            ('status', '=', 'available')
            ], order='borrow_count desc', limit=3)
        final_books = book_author | book_genre | popular_books
        results['recommendation_ids'] = [Command.set(final_books.ids)]

        return results

    # confirm button inside wizard
    def action_recommend_confirm(self):
        active_id = self.env.context.get('active_id')
        checkout = self.env['checkouts'].browse(active_id)
        if self.recommendation_ids.ids:
            for book in self.recommendation_ids:
                self.env['checkout.line'].create({
                    'check_ids': checkout.id,
                    'borrowed_book_id': book.id,
                })
            book.status = 'unavailable'
            checkout.status = 'checkout'
            l=checkout.borrower_id.maximum_books_in_single_checkout

            already_in_checkout = len(checkout.checkouts_line_ids)

            T = already_in_checkout
            if T > l:
                raise ValidationError(f'You cannot borrow more than {T} book')

        else :
            raise ValidationError('you cannot confirm as suggestion books are empty')

