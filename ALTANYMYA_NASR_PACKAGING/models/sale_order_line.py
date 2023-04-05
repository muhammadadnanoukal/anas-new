from odoo import fields, models


class SaleOrderLineNasr(models.Model):
    _inherit = 'sale.order.line'
    job_type = fields.Selection([("repeat", "Repeat"), ("revised", "Revised"), ("new", "New")], default='new')
