# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
from datetime import timedelta
import logging
from odoo import Command

_logger = logging.getLogger(__name__)


def getDate():
    today = date.today()
    new_date = today + relativedelta(months=+1)
    return new_date


class Checkouts(models.Model):
    _name = 'checkouts'
    _description = 'Checkouts'
    _rec_name = 'check'
    _order = "check desc"

    check = fields.Char(string='Checkout ID', default=lambda self: _('New'))
    customer_email = fields.Char(string='customer email')
    checkout_count = fields.Integer(compute='_compute_count',string='count of previous checkouts',default=0)
    borrower_id = fields.Many2one('members', string='Borrower')
    borrower_phone = fields.Char(related='borrower_id.member_id.phone', string='Borrowers Phone')
    book_id = fields.Many2one('books', string='Book Id')
    borrowed_book_name = fields.Text(related='checkouts_line_ids.borrowed_book_id.book_name', string='Book Name')
    checkout_date = fields.Datetime(string='Checkout Date', default=fields.Date.today())
    due_date = fields.Datetime(string='Due date', compute='_compute_due_date' ,default=getDate(), store=True)
    status = fields.Selection(
        selection=[('draft', 'Draft'), ('checkout', 'Checkout'), ('returned', 'Returned'), ('overdue', 'Overdue')],
        default='draft'
    )
    return_date = fields.Datetime(string='Return date',default=fields.Date.today(),store=True)
    penalties = fields.Integer(compute="_compute_penalties", string='Penalties of 50/-', store=True)
    checkouts_line_ids = fields.One2many('checkout.line', 'check_ids')
    late_status = fields.Selection(
        string="late status",
        selection=[('late','Late'),('on_time','On Time')],
        store=True
    )
    late_returns = fields.Char(compute='_compute_late_status',store=True)
    invoice_id = fields.Many2one('account.move')
    book_status_update = fields.Boolean(compute='update_book_status',store=True)
    pay_state = fields.Selection(
        selection=[('paid','Paid'),('not_paid','Not Paid')],
        compute='_compute_state',
        default='not_paid',
        store=True,
        readonly=True
    )
    @api.depends('borrower_id')
    def _compute_count(self):
        f=self.env['checkouts'].search_count([
            ('borrower_id','=',self.borrower_id.id)
        ])
        self.checkout_count = f-1



    @api.onchange('borrower_id')
    def onchange_warning_late_returns(self):
      for record in self:
        late_count = self.env['ir.config_parameter'].sudo().get_param('library.late_returns_maximum')
        l_c = self.env['checkouts'].search_count([
            ('borrower_id', '=', record.borrower_id.id),
            ('late_status', '=', 'late')
        ])
        if l_c >= int(late_count)-1 and l_c < int(late_count):
            return {
                'warning': {
                    'title': _("warning"),
                    'message': _(" This member has high number of late returns ")
                }
            }


    @api.depends('due_date', 'return_date')
    def _compute_late_status(self):
        for record in self:
            if record.due_date and record.return_date:
                late = (record.return_date - record.due_date).total_seconds()
                late_days = int(late / 3600)
                if late_days <= 0:
                    record.late_status = 'on_time'
                else:
                    record.late_status = 'late'
            else:
                record.late_status = 'on_time'




    @api.depends('due_date', 'checkout_date')
    def _compute_due_date(self):
        for record in self:
            if record.due_date and record.checkout_date:
               record.due_date = record.checkout_date + relativedelta(months=+1)



    # to compute penalties
    @api.depends('due_date','return_date')
    def _compute_penalties(self):
        for record in self:
            p_per_hour = int(self.env['ir.config_parameter'].sudo().get_param('library.penalty_per_hour'))
            if record.return_date and record.due_date:
                if (record.return_date - record.due_date).total_seconds() > 0:
                    w = (record.return_date - record.due_date).total_seconds()
                    per_hour = int(w / 3600)
                    penalty_per_hour = p_per_hour * int(per_hour)
                    record.penalties =  float(penalty_per_hour)



    # to create return function
    def return_book(self):
        self.status = 'returned'


    # to create checkout function
    def checkout_book(self):
        self.ensure_one()

        if self.status == 'checkout':
            raise ValidationError('Book is already confirmed')
        self.write({'status': 'checkout'})
        for record in self:
            today = fields.Datetime.today()
            if not record.borrower_id:
                raise ValidationError("select a member.")
            limit = record.borrower_id.maximum_book
            already_issued = self.search_count([
                ('borrower_id', '=', record.borrower_id.id),
                '|', ('status', '=', 'checkout'), ('status', '=', 'returned')])
            total_checkouts = already_issued + 1
            if total_checkouts > int(limit):
                raise ValidationError(f"You have reached maximum of {limit} borrow  limit.")
            overdue_books = self.env['checkouts'].search_count([
                ('borrower_id', '=', record.borrower_id.id),
                ('due_date','<',today),
                ('status','!=','returned')

            ])
            if overdue_books >= 1 :
                raise ValidationError('you have overdue books to be returned')
            record.status = 'checkout'
            record.checkouts_line_ids.mapped('borrowed_book_id').write({'status': 'unavailable'})
            maximum_books_by_default = record.borrower_id.maximum_books_in_single_checkout
            if len(self.checkouts_line_ids) > int(maximum_books_by_default):
                raise ValidationError(f'You cannot borrow more than {maximum_books_by_default} book')
            late_count = self.env['ir.config_parameter'].sudo().get_param('library.late_returns_maximum')
            l_c = self.env['checkouts'].search_count([
                ('borrower_id','=',record.borrower_id.id),
                ('late_status','=','late')
            ])
            if int(late_count) <= l_c:
                raise ValidationError(f'You have crossed maximum no of late return of books')

        return {
        'type': 'ir.actions.act_window',
        'name': 'Book Recommendation',
        'res_model': 'book.recommendation',
        'view_mode': 'form',
        'target': 'new',
        'context': {
            'active_id': self.id,

        }
    }




    def action_invoice_view(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'invoice',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('checkout_id', '=', self.id),('payment_state','=','paid')],
            'context': {'invoice_id': self.id}

        }


    def cancel_book(self):
        if self.status == 'checkout':
            self.checkouts_line_ids.mapped('borrowed_book_id').write({'status': 'available'})



    def create(self, vals):
        if vals.get('check', _('New')) == _('New'):
            vals['check'] = self.env['ir.sequence'].next_by_code('checkouts') or _('New')
        return super().create(vals)



    @api.model
    def send_notification(self):
        today = fields.Date.today()
        reminder_days = int(self.env['ir.config_parameter'].sudo().get_param('library.remainder_days', default=0))
        reminder_date = today + timedelta(days=reminder_days)
        notify_template = self.env.ref(
            'library.email_template_reminder_days',
            raise_if_not_found=False
        )
        if not notify_template:
            return
        checkouts_to_notify = self.env['checkouts'].search([
            ('due_date', '=', reminder_date),
            ('status', '=', 'checkout')
        ])
        for record in checkouts_to_notify:
            notify_template.send_mail(record.id, force_send=True)




    def overdue_checkout(self):
      for record in self:
        today = fields.Date.today()
        if today > record.due_date and self.status != 'returned':
            self.status = 'overdue'



    def create_invoice(self):
        penalty_amt = self.env.ref('library.penalty_ddd')
        list=[]
        for record in self:
            for r in record.checkouts_line_ids:
               list .append(Command.create({
                            'product_id': r.borrowed_book_id.prd_id.id,
                            'price_unit': r.borrowed_book_id.prd_id.list_price,
                            'quantity': 1,
                        }))
            list.append(Command.create({
                'product_id': penalty_amt.id,
                'price_unit': record.penalties,
                'quantity': 1,
            }))
        invoice = self.env['account.move'].create({
                'partner_id': record.borrower_id.member_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids' : list,
                 'checkout_id':record.id,
        })
        record.invoice_id = invoice.id
        return {
            'type' : 'ir.actions.act_window',
            'name' : 'invoice for books',
            'res_model' : 'account.move',
             'res_id' : invoice.id,
            'view_mode' : 'form',
            'target' : 'current'

        }


    @api.depends('invoice_id.payment_state')
    def update_book_status(self):
        for record in self:
             if record.invoice_id.payment_state == 'paid':
                 self.checkouts_line_ids.mapped('borrowed_book_id').write({'status': 'available'})



    @api.depends('invoice_id.payment_state','pay_state')
    def _compute_state(self):
        for record in self:
            if record.invoice_id.payment_state == 'paid':
                record.pay_state = record.invoice_id.payment_state
