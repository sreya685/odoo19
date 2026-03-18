from odoo import api,fields,models

class ReportWizard(models.TransientModel):
    _name = 'report.wizard'
    _description = 'Wizard Report'
    # reference_id = fields.Char('Reference ID')
    book_name = fields.Char('Book name')
    author_name = fields.Char('Author name')
    checkout_date = fields.Datetime('Checkout date')
    return_date = fields.Datetime('Return date')
    genres_type = fields.Char('genres types')
    def print_pdf_button(self):
        query = """select bk.book_name,at.author_name,gn.genre_types,ch.check,ch.checkout_date,ch.return_date from checkouts as ch
                  inner join checkout_line as chl on chl.check_ids = ch.id
                  inner join books as bk on bk.id = chl.borrowed_book_id
                  inner join authors as at on at.id = bk.authors_id
                  inner join genres as gn on gn.id = bk.genres_id
                  
                  """
        # if self.checkout_date :
        #     query += """ where ch.checkout_date = '%s' """%(self.checkout_date)
        # if self.return_date :
        #     query += """ or ch.return_date = '%s' """%(self.return_date)
        # if self.genres_type :
        #     query += """ or gn.genre_types = '%s' """%(self.genres_type)
        # if self.author_name :
        #     query += """ or at.author_name = '%s' """%(self.author_name)
        # if self.book_name :
        #     query += """ or bk.book_name = '%s' """%(self.book_name)
        print('query : ',query)
        self.env.cr.execute(query)

        report = self.env.cr.dictfetchall()
        print('repo : ',report)

        data = {'date': self.read()[0], 'report': report}
        return self.env.ref('library.report_book_borrow_action').report_action(None, data=data)
    #
    # inner join books as bk on bk.id = chl.borrowed_book_id
    # inner join authors as at on at.id = bk.authors_id
    # inner join genres as gn on gn.id = bk.genres_id
    # query = """select ch.checkout_date,ch.return_date from checkouts as ch"""
    # if self.reference_id:
    #     query += """ where bk.reference_id == '%s'""" % self.reference_id
    # if self.book_name:
    #     query += """ where bk.book_name == '%s'""" % self.book_name
    # if self.author_name:
    #     query += """ where at.author_name == '%s'""" % self.author_name
    # query += """ where 1=1 """
    # p=[]
    # if self.return_date:
    #     query += """ where ch.return_date <= '%s'""" % self.return_date
    # if self.genres_type:
    #     query += """ where gn.genre_types == '%s'""" % self.genres_type
    # [data] = self.read()
    # data['emp'] = self.env.context.get('active_ids', [])
    # check = self.env['checkouts'].browse(data['emp'])
    # rec = self.env['checkouts'].browse(report[0])



