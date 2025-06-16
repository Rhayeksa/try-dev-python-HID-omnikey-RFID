# models/latihan_model.py
from odoo import api, fields, models


class Tree(models.Model):
    _name = 'tree.model'
    _description = 'Tree Model'

    name = fields.Char(string="Name", required=True)
    rfid_tag = fields.Char(string="RFID Tag", required=True)
    species = fields.Selection([
        ("kelapa sawit", "Kelapa Sawit"),
        ("karet", "Karet"),
        ("kopi", "Kopi"),
        ("teh", "Teh"),
        ("kelapa", "Kelapa"),
        ("pinang", "Pinang"),
        ("tebu", "Tebu"),
    ], string="Species")
    planting_date = fields.Date(string="Planting Date")
    deskripsi = fields.Text(string="Deskripsi")

    age = fields.Integer(string="Age (Days)", default=0)
    age_display = fields.Char("Age Display", compute="_compute_age_display")
    datetime_check = fields.Datetime(string="Datetime Check")
    counter_check = fields.Integer(string="Counter Check", default=0)

    @api.depends('age')
    def _compute_age_display(self):
        for rec in self:
            rec.age_display = f"{rec.age} hari" if rec.age is not None else "-"
