from odoo import http
from odoo.http import request

class BestSellerSnippet(http.Controller):
    @http.route('/get_best_sellers', auth="public", type='jsonrpc',
                website=True)
    def get_best_seller(self):
        """Get the website categories for the snippet."""
        best_sellers = request.env['books'].sudo().search_read(
            [('parent_id', '=', False)], fields=['book_name', 'image_1920', 'isbn','price']
        )
        values = {
            'books': best_sellers,
        }
        print(values)
        return values
