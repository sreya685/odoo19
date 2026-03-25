import io
import json
from datetime import datetime, date
from odoo import fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools import date_utils, json_default
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

class XLSXReportWizard(models.TransientModel):
    """ Wizard for Employee Attendance Report """
    _name = 'xlsx.report.wizard'
    _description = 'Book Borrow XLSX Report Wizard'

    mem_id = fields.Many2one('members', string="Members")
    book_name = fields.Many2one('books',string='Book Name')
    author_name = fields.Many2one('authors',string='Author Name')
    checkout_date = fields.Datetime('Checkout date')
    return_date = fields.Datetime('Return date')
    genres_type = fields.Many2one('genres',string='Genres Type')
    sort_by = fields.Selection(
        string='sort by',
        selection=[('checkout_date', 'Checkout Date'), ('return_date', 'Return Date')
                   ]
    )
    order = fields.Selection(
        string='order',
        selection=[('asc', 'Asc'), ('desc', 'Desc')]
    )
    def action_print_xlsx(self):
        """
        Returns report action for the XLSX Attendance report
        Raises: ValidationError: if From Date > To Date
        Raises: ValidationError: if there is no attendance records
        Returns:
            dict:  the XLSX report action
        """

        data = {
            'checkout_date': self.checkout_date,
            'return_date': self.return_date,
            'book_name': self.book_name.id,
            'author_name': self.author_name.id,
            'genre_types': self.genres_type.id,
            'mem_id': self.mem_id.id,
            'sort_by': self.sort_by,
            'order': self.order
        }
        if self.checkout_date or self.return_date  or self.genres_type.id or self.mem_id.id or self.book_name.id or self.author_name.id or self.sort_by or self.order or 1:
          return {
                'type': 'ir.actions.report',
                'data': {'model': 'xlsx.report.wizard',
                         'options': json.dumps(data, default=json_default),
                         'output_format': 'xlsx',
                         'report_name': 'Book Borrow XLSX Report',
                         },
                'report_type': 'xlsx',
            }
    def get_xlsx_report(self, data, response):
        """
        Print the XLSX report
        Returns: None
        """
        query = """select bk.book_name,bk.language,at.author_name,gn.genre_types,rp.name as borrower_name,ch.check,ch.checkout_date,ch.return_date from checkouts as ch
                      inner join checkout_line as chl on chl.check_ids = ch.id
                      inner join books as bk on bk.id = chl.borrowed_book_id
                      inner join authors as at on at.id = bk.authors_id
                      inner join genres as gn on gn.id = bk.genres_id
                      inner join members as me on me.id = ch.borrower_id
                      inner join res_partner as rp on rp.id = me.member_id
                      where 1=1

                      """

        if data.get('checkout_date'):
            query += """ and date(ch.checkout_date) >= date '%s' """ % data['checkout_date']
        if data.get('return_date'):
            query += """ and date(ch.return_date) <= date '%s' """ % data['return_date']
        if data.get('genres_type'):
            query += """ and gn.id = '%s' """ % data['genre_types']
        if data.get('author_name'):
            query += """ and at.id = '%s' """ % data['author_name']
        if data.get('book_name'):
            query += """ and bk.id = '%s' """ % data['book_name']
        if data.get('mem_id'):
            query += """ and ch.borrower_id = '%s' """ % data['mem_id']
        if data.get('sort_by') == 'checkout_date':
            query += """ order by checkout_date"""
        elif data.get('sort_by') == 'return_date':
            query += """ order by return_date"""
        if data.get('order') == 'asc':
            query += """ asc"""
        elif data.get('order') == 'desc':
            query += """ desc"""

        print('query',query)
        self.env.cr.execute(query)
        docs = self.env.cr.dictfetchall()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Book Borrow Report')
        sheet.set_column(2, 2, 15)
        sheet.set_column(2, 3, 15)
        sheet.set_column(2, 4, 15)
        sheet.set_column(2, 5, 15)
        sheet.set_column(2, 6, 15)
        sheet.set_column(2, 7, 15)
        sheet.set_column(2, 2, 15)

        border = workbook.add_format({'font_size': 10, 'align': 'center','border': 1})

        head = workbook.add_format(
            {'bold': True, 'font_size': 10, 'align': 'center','border': 1})
        date = workbook.add_format(
            {'num_format': 'yyyy-mm-dd','font_size': 10, 'align': 'center','border': 1}
        )
        row=4
        for d in docs:
            col = 2
            if data['book_name']:
              sheet.write(row,col,'Book Name',border)
              col += 1
              sheet.write(row,col,d.get('book_name'), border)
              row += 1
            col = 2

            if data['author_name']:
              sheet.write(row,col, 'Author Name', border)
              col +=1
              sheet.write(row,col,d.get('author_name'), border)
              row += 1
            col = 2

            if data['genre_types']:
              sheet.write(row,col, 'Genre Type', border)
              col +=1
              sheet.write(row,col,d.get('genre_types'), border)
              row += 1

            col = 2
            if data['checkout_date']:
              sheet.write(row,col, 'Checkout Date', border)
              col +=1
              sheet.write(row,col,d.get('checkout_date'), date)
              row += 1

            col = 2
            if data['return_date']:
              sheet.write(row,col, 'Return Date', border)
              col +=1
              sheet.write(row,col,d.get('return_date'), date)
              row += 1

            col = 2
            if data['mem_id']:
              sheet.write(row,col, 'Borrower Name', border)
              col +=1
              sheet.write(row,col,d.get('borrower_name'), border)

        # header=[
        #     'Book Name','Author Name','Genre Type','Checkout ID','Borrower Name','Checkout Date', 'Return Date'
        # ]
        # sheet.write(3,4,'CHECKOUT REPORT',head)
        sheet.merge_range('E2:F2', 'CHECKOUT REPORT', head)
        row = 11
        col = 2

        if data.get('book_name'):
                sheet.write(row, col, ' ', head)
        else:
                sheet.write(row, col, 'Book Name', head)
                col += 1
        if data.get('author_name'):
                sheet.write(row, col, ' ', head)
        else:
                sheet.write(row, col, 'Author Name', head)
                col += 1
        if data.get('genre_types'):
                sheet.write(row, col, ' ', head)
        else:
                sheet.write(row, col, 'Genre Type', head)
                col += 1

        sheet.write(row, col, 'Checkout ID', head)
        col += 1
        if data.get('mem_id'):
                sheet.write(row, col, ' ', head)
        else:
                sheet.write(row, col, 'Borrower Name', head)
                col += 1
        if data.get('checkout_date'):
                sheet.write(row, col, ' ', head)
        else:
                sheet.write(row, col, 'Checkout Date', head)
                col += 1
        if data.get('return_date'):
                sheet.write(row, col, ' ', head)
        else:
                sheet.write(row, col, 'Return Date', head)
                col += 1


        row = 11

        for d in docs:
            col = 2
            row += 1
            if data.get('book_name'):
                sheet.write(row, col, ' ', border)
            else:
                sheet.write(row,col, d.get('book_name'), border)
                col += 1
            if data.get('author_name'):
                sheet.write(row, col, ' ', border)
            else:
                sheet.write(row,col, d.get('author_name'),border)
                col += 1
            if data.get('genre_types'):
                sheet.write(row, col, ' ', border)
            else:
                sheet.write(row,col, d.get('genre_types'),border)
                col += 1
            sheet.write(row,col, d.get('check'), border)
            col += 1
            if data.get('mem_id'):
                sheet.write(row, col, ' ', border)
            else:
                sheet.write(row,col, d.get('borrower_name'),border)
                col += 1
            if data.get('checkout_date'):
                sheet.write(row, col, ' ', border)
            else:
                sheet.write(row, col, d.get('checkout_date'), date)
                col += 1
            if data.get('return_date'):
                sheet.write(row, col, ' ', border)
            else:
                sheet.write(row, col, d.get('return_date'), date)
                col += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
