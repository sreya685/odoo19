from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo import http
from odoo.http import request

class CustomPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        return values
    @http.route(['/my/books','/my/books/page/<int:page>'], type='http', auth="public", website=True)
    def portal_my_books(self,**kw):
        # values = super()._prepare_home_portal_values(counters)
        books = request.env['books'].sudo().search([
            ('create_uid','=', request.env.user.id)

                ])

        return request.render('library.portal_page_template',{'books':books})

