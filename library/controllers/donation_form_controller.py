from odoo import http
from odoo.http import request

class WebsiteCustomerForm(http.Controller):
    @http.route(['/website/customer/form'], type='http', auth="public", website=True)
    def customer_form(self, **kw):
        return request.render('library.donation_form_template')
    @http.route(['/website/customer/create'], type='http', auth="public", methods=['POST'], website=True, csrf=True)
    def create_customer(self, **post):
        # pp=[]
        # pp.append(request.env['authors'].sudo().create({
        #     'author_name': post.get('author_name')
        # }))
        request.env['books'].sudo().create({
            'book_name': post.get('book_name'),
            # 'authors_id': post.get('authors_id.author_name'),
            'status' : post.get('status'),
            'image_1920': post.get('image_1920'),
            'description': post.get('description'),
        })
        return request.render('library.donation_success_template')
