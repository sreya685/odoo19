from odoo import api,fields,models
import datetime

class ReportWizard(models.TransientModel):
    _name = 'report.wizard'
    _description = 'Wizard Report'

    mem_id = fields.Many2one('members',string="Members")
    book_name = fields.Many2one('books')
    author_name = fields.Many2one('authors')
    checkout_date = fields.Datetime('Checkout date')
    return_date = fields.Datetime('Return date')
    genres_type = fields.Many2one('genres')
    sort_by = fields.Selection(
        string= 'sort by',
        selection=[ ('checkout_date','Checkout Date'),('due date','Due Date')
                    ]
    )
    order = fields.Selection(
        string='order',
        selection=[('asc','Asc'),('desc','Desc')]
    )
    def print_pdf_button(self):
        query = """select bk.book_name,bk.language,at.author_name,gn.genre_types,ch.check,ch.checkout_date,ch.return_date from checkouts as ch
                  inner join checkout_line as chl on chl.check_ids = ch.id
                  inner join books as bk on bk.id = chl.borrowed_book_id
                  inner join authors as at on at.id = bk.authors_id
                  inner join genres as gn on gn.id = bk.genres_id
                  where 1=1
                  
                  """

        if self.checkout_date :
            query += """ and date(ch.checkout_date) >= date '%s' """%(self.checkout_date)
        if self.return_date :
            query += """ and date(ch.return_date) <= date '%s' """%(self.return_date)
        if self.genres_type :
            query += """ and gn.id = '%s' """%(self.genres_type.id)
        if self.author_name :
            query += """ and at.id = '%s' """%(self.author_name.id)
        if self.book_name :
            query += """ and bk.id = '%s' """%(self.book_name.id)
        if self.mem_id:
            query += """ and ch.borrower_id = '%s' """%(self.mem_id.id)
        if self.sort_by == 'checkout_date':
            query += """ order by checkout_date"""
        elif self.sort_by == 'due date':
            query += """ order by due_date"""
        if self.order == 'asc':
            query += """ asc"""
        elif self.order == 'desc':
            query += """ desc"""

        print('query : ',query)
        self.env.cr.execute(query)

        report = self.env.cr.dictfetchall()
        print('repo : ',report)

        data = {'date': self.read()[0], 'report': report}
        return self.env.ref('library.report_book_borrow_action').report_action(self, data=data)
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



