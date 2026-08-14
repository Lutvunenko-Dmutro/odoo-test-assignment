from odoo import models, fields

class TCK(models.Model):
    _name = 'company_hr_military.tck'
    _description = 'ТЦК та СП'

    name = fields.Char(string='Назва ТЦК та СП', required=True)
    code = fields.Char(string='Код')
    phone = fields.Char(string='Телефон')
