from odoo import fields, models


class ProductTemplateNasr(models.Model):
    _inherit = 'product.template'
    outs = fields.Integer(string="Ups")
    color = fields.Integer(string="Color")
    coating = fields.Char(string="Coating")
    gsm_substance = fields.Float(string="GSM")
    sub_category = fields.Many2one('product.category', string="Category")
    process = fields.Char(string="Production Process")
    sheet_width = fields.Char(string="Sheet Width")
    sheet_length = fields.Char(string="Sheet Length")
    sheet_width_cut = fields.Char(string="Sheet Width Cut Amount", default='1.5')
    sheet_length_cut = fields.Char(string="Sheet Length Cut Amount", default='1.5')
    pack_qty = fields.Char(string="Pack Quantity")
