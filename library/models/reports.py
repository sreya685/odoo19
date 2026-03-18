# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Report(models.Model):
    _name = 'reports'
    _description = 'Reports'


    # report_id = fields.Integer('report ID')

    def action_report_wizard(self):
      return {
        'type': 'ir.actions.act_window',
        'name': 'Book Borrow Report',
        'res_model': 'report.wizard',
        'view_mode': 'form',
        'target': 'new',
        'context': {
            'active_id': self.id,

        }
    }