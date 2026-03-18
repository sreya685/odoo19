# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Tags(models.Model):
    _name = 'tags'
    _description = 'Tags'
    _rec_name = "tag_name"
    tag_name = fields.Char(string='Tag Name')