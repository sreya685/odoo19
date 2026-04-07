from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request
import user,counters




class PortalAccount(CustomerPortal):
   def _prepare_home_portal_values(self, counters):
       values = super()._prepare_home_portal_values(counters)

       if user.has_group('partner_loan_management.partner_loan_manager'):
               if 'books' in counters:
                   books = request.env['books'].search(
                       [('status', '=', 'available')])
                   values['books'] = books
       else:
               if 'books' in counters:
                   books = request.env['books'].search(
                       [('partner_id', '=', user.partner_id.id),
                        ('state', '=', 'available')])
                   values['books'] = books
       return values
