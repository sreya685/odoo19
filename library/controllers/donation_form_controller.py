import base64

from odoo import http,Command
from odoo.http import request

class WebsiteCustomerForm(http.Controller):
    @http.route(['/website/customer/form'], type='http', auth="public", website=True)
    def customer_form(self, **kw):
        return request.render('library.donation_form_template')
    @http.route(['/website/customer/create'], type='http', auth="public", website=True, csrf=True)
    def create_customer(self, **kw):
        print(kw)
        # img_data = False
        # att=[]
        # if kw.get('attachment'):
        #     for i in kw.get('attachment'):
        #           img_data = i[0]
        #           att.append(i.read())
        #
        # print(att)
        # print(img_data)
        # files = request.httprequest.files.getlist('attachment')
        # print(files)
        # img_data = False
        # other_img = []
        # for i,file in enumerate(files):
        #
        #     if i == 0:
        #         img_data = file
        #     else:
        #         other_img.append(Command.create({
        #             'images': file
        #         }))

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
            # 'book_image': base64.b64encode(att),
            'description': kw.get('description'),
            'user_id': self.env.user.id,
        })
        return request.render('library.donation_success_template')


