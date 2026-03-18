# -*- coding: utf-8 -*-
from odoo import models,fields,api


class Genres(models.Model):
    _name ='genres'
    _description ='Genres'
    _rec_name = 'genre_types'

    genre_types =fields.Char(string='Genres')
    description  = fields.Text(string='Description')

