# models/latihan_model.py
from odoo import fields, models


class LatihanModel(models.Model):
    _name = 'latihan.model'
    _description = 'Model Latihan'

    name = fields.Char(string='Nama', required=True)
    deskripsi = fields.Text(string='Deskripsi')
    tanggal = fields.Date(string='Tanggal')
