from odoo import http
from odoo.http import request

class WebsitePortalForm(http.Controller):
    @http.route(['/website/portal/form'], type='http', auth="public", website=True)
    def portal_form(self, **kw):
        books = request.env['books'].sudo().search([
            ('user_id','=', self.env.user.id)

                ])

        return request.render('library.portal_page_template',{'books':books})
    # @http.route(['/website/portal/create'], type='http', auth="public", website=True, csrf=True)
    # def create_portal(self, **post):
    #     books = request.env['books'].sudo().search({
    #         'user_id': self.env.user
    #
    #     })
    #     print(books)
    #     return request.render('library.portal_page_template',{'books':books})
