import base64

from odoo import http
from odoo.http import request

class WebsiteCustomerForm(http.Controller):
    @http.route(['/website/customer/form'], type='http', auth="public", website=True)
    def customer_form(self, **kw):
        return request.render('library.donation_form_template')
    @http.route(['/website/customer/create'], type='http', auth="public", website=True, csrf=True)
    def create_customer(self, **kw):
        print(kw)
        # img_file = request.httprequest.files.get('ufile')
        # print('tes :',img_file)
        # if img_file:
        #    img_data = base64.b64encode(img_file.read())
        #    print('value :',img_data)
        if kw.get('attachment'):
                attachment = kw.get('attachment').read()
        pp = request.env['authors'].sudo().create({
            'author_name': kw.get('author_name')
        })
        request.env['books'].sudo().create({
            'book_name': kw.get('book_name'),
            'authors_id':pp.id,
            'condition' : kw.get('condition'),
            'image_1920': base64.b64encode(attachment),
            # 'image_1920': img_data,
            'description': kw.get('description'),
            'user_id': self.env.user.id,
        })
        return request.render('library.donation_success_template')


