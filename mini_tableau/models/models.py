# -*- coding: utf-8 -*-
from odoo import models, fields, api, os


class MiniTableau(models.Model):
    _name = 'mini.tableau'
    _description = 'mini.tableau'

    user_query = fields.Char(string="User Query")
    report_name = fields.Char(string="Report Name")
    report_rows = fields.Char(string="Rows")
    report_columns = fields.Char(string="Columns")
    chart_type = fields.Char(string="Chart Type", default="None")
