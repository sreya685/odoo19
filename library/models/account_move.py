# -*- coding: utf-8 -*-
from odoo import api, models, fields


class AccountMove(models.Model):
    _inherit = "account.move"

    checkout_id = fields.Many2one('checkouts')



