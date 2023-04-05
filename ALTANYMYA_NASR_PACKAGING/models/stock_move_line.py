from odoo import fields, models


class StockMoveLineNasr(models.Model):
    _inherit = 'stock.move.line'
    pallet = fields.Integer(string="Pallet Number", default=1)

