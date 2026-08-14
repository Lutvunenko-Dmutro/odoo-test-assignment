from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_reserved = fields.Boolean(string='Бронювання', default=False)
    is_mobilized = fields.Boolean(string='Мобілізований', default=False)
    tck_id = fields.Many2one('company_hr_military.tck', string='ТЦК та СП')
    edrpvr_number = fields.Char(string='№ в ЄДРПВР')
