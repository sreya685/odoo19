import io
import json
from datetime import datetime, date
from dateutil.rrule import rrule, DAILY
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
    # from_date = fields.Date('From Date', help="Starting date for report")
    # to_date = fields.Date('To Date', help="Ending date for report")
    # employee_ids = fields.Many2many('hr.employee', string='Employee',
    #                                 help='Name of Employee')
    mem_id = fields.Many2one('members', string="Members")
    book_name = fields.Many2one('books')
    author_name = fields.Many2one('authors')
    checkout_date = fields.Datetime('Checkout date')
    return_date = fields.Datetime('Return date')
    genres_type = fields.Many2one('genres')
    sort_by = fields.Selection(
        string='sort by',
        selection=[('checkout_date', 'Checkout Date'), ('due date', 'Due Date')
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
            'genre_type': self.genres_type.id,
        }

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
        query = """select bk.book_name,bk.language,at.author_name,gn.genre_types,ch.check,ch.checkout_date,ch.return_date from checkouts as ch
                      inner join checkout_line as chl on chl.check_ids = ch.id
                      inner join books as bk on bk.id = chl.borrowed_book_id
                      inner join authors as at on at.id = bk.authors_id
                      inner join genres as gn on gn.id = bk.genres_id
                      where 1=1

                      """

        if self.checkout_date:
            query += """ and date(ch.checkout_date) >= date '%s' """ % (self.checkout_date)
        if self.return_date:
            query += """ and date(ch.return_date) <= date '%s' """ % (self.return_date)
        if self.genres_type:
            query += """ and gn.id = '%s' """ % (self.genres_type.id)
        if self.author_name:
            query += """ and at.id = '%s' """ % (self.author_name.id)
        if self.book_name:
            query += """ and bk.id = '%s' """ % (self.book_name.id)
        if self.mem_id:
            query += """ and ch.borrower_id = '%s' """ % (self.mem_id.id)
        if self.sort_by == 'checkout_date':
            query += """ order by checkout_date"""
        elif self.sort_by == 'due date':
            query += """ order by due_date"""
        if self.order == 'asc':
            query += """ asc"""
        elif self.order == 'desc':
            query += """ desc"""
        # query = """select hr_e.name,date(hr_at.check_in),
        #     SUM(hr_at.worked_hours) from hr_attendance hr_at LEFT JOIN
        #     hr_employee hr_e ON hr_at.employee_id = hr_e.id"""
        # if not data['employee_ids']:
        #     query += """ GROUP BY date(check_in), hr_e.name"""
        # else:
        #     query += """ WHERE hr_e.id in (%s) GROUP BY date(check_in),
        #     hr_e.name""" % (', '.join(str(employee_id)
        #                               for employee_id in data['employee_ids']))
        self.env.cr.execute(query)
        docs = self.env.cr.dictfetchall()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('docs')
        start_date = datetime.strptime(data['checkout_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['return_date'], '%Y-%m-%d').date()
        date_range = rrule(DAILY, dtstart=start_date, until=end_date)
        sheet.set_column(1, 1, 15)
        sheet.set_column(2, 2, 15)
        border = workbook.add_format({'border': 1})
        # green = workbook.add_format({'bg_color': '#28A828', 'border': 1})
        # red = workbook.add_format({'bg_color': '#ff3333', 'border': 1})
        # rose = workbook.add_format({'bg_color': '#DA70D6', 'border': 1})
        head = workbook.add_format(
            {'bold': True, 'font_size': 30, 'align': 'center'})
        date_size = workbook.add_format(
            {'font_size': 12, 'bold': True, 'align': 'center'})
        sheet.merge_range('C3:K6', 'Book Borrow Report', head)
        sheet.merge_range('B8:C9', 'From Date: ' + data['checkout_date'], date_size)
        sheet.merge_range('B10:C11', 'To Date: ' + data['return_date'], date_size)
        # sheet.write(2, 12, '', green)
        # sheet.write(2, 13, 'Present')
        # sheet.write(4, 12, '', red)
        # sheet.write(4, 13, 'Absent')
        # sheet.write(6, 12, '', rose)
        # sheet.write(6, 13, 'Half Day')
        sheet.merge_range('B16:B17', 'Sl.No', border)
        sheet.merge_range('C16:C17', 'Checkouts', border)
        row = 15
        col = 2
        for date_data in date_range:
            col += 1
            sheet.write(row, col, date_data.strftime('%Y-%m-%d'), border)
        # row = 16
        # col = 2
        # for date_data in date_range:
        #     col += 1
        #     sheet.write(row, col, date_data.strftime('%a'), border)
        # employee_names = []
        # attendance_list = []
        # for doc in docs:
        #     if doc['name'] not in employee_names:
        #         date_sum_list = []
        #         employee_names.append(doc['name'])
        #         for date_data in date_range:
        #             date_out = date_data.strftime('%Y-%m-%d')
        #             record_list = list(
        #                 filter(
        #                     lambda x: x['name'] == doc['name'] and x[
        #                         'date'].strftime(
        #                         '%Y-%m-%d') == date_out, docs))
        #             if record_list:
        #                 date_sum_list.append(record_list[0])
        #             else:
        #                 date_sum_list.append({
        #                     'name': '',
        #                     'date': '',
        #                     'sum': 0
        #                 })
        #         attendance_list.append(
        #             {'name': doc['name'], 'items': date_sum_list})
        # work = self.env.ref('resource.resource_calendar_std')
        # row = 17
        # i = 0
        # for rec in attendance_list:
        #     row += 1
        #     col = 1
        #     i += 1
        #     sheet.write(row, col, i, border)
        #     col += 1
        #     sheet.write(row, col, rec['name'], border)
        #     for item in rec['items']:
        #         col += 1
        #         if item['sum'] >= work.hours_per_day:
        #             sheet.write(row, col, item['sum'], green)
        #         elif 1 <= item['sum'] <= 4 or 4 <= item['sum'] <= \
        #                 work.hours_per_day:
        #             sheet.write(row, col, item['sum'], rose)
        #         else:
        #             sheet.write(row, col, item['sum'], red)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
