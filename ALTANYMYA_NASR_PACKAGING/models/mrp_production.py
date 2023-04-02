from odoo import api, fields, models


class MrpProductionNasr(models.Model):
    _inherit = 'mrp.production'

    sale_order_id = fields.Many2one('sale.order', string='Sale Order', compute='_compute_sale_order_id')
    sale_order_line_id = fields.Many2one('sale.order.line', string="Sale Order Line",
                                         compute='_compute_sale_order_line_id')

    hide = fields.Boolean(string='Hide', compute="_compute_hide")
    sale_order_partner_id = fields.Char(string='Customer', compute='_compute_sale_order_partner_id')
    sale_order_client_order_ref = fields.Char(string='Customer Reference',
                                              compute='_compute_sale_order_client_order_ref')
    delivery_date = fields.Datetime(string="Delivery On", compute="_compute_delivery_date")
    impression = fields.Integer(string="Impression", compute="_compute_impression")
    color_quality = fields.Char(string="Color Quality", compute="_compute_color_quality")
    board = fields.Char(string="Board", compute="_compute_board")
    board_gsm = fields.Char(string="Board Gsm", compute="_compute_board_gsm")
    sheet_size = fields.Char(string="Sheet Size", compute="_compute_sheet_size")
    cut_size = fields.Char(string="Cut Size", compute="_compute_cut_size")

    @api.depends('product_id')
    def _compute_cut_size(self):
        for rec in self:
            cut_width = float(rec.product_id.sheet_width) - float(rec.product_id.sheet_width_cut)
            cut_length = float(rec.product_id.sheet_length) - float(rec.product_id.sheet_length_cut)
            rec.cut_size = str(cut_width) + " X " + str(cut_length)

    @api.depends('product_id')
    def _compute_sheet_size(self):
        for rec in self:
            rec.sheet_size = str(rec.product_id.sheet_width) + " X " + str(rec.product_id.sheet_length)

    @api.depends('product_id')
    def _compute_board_gsm(self):
        for rec in self:
            rec.board_gsm = str(rec.product_id.gsm_substance) + " " + str(rec.board)

    @api.depends('product_id')
    def _compute_board(self):
        for rec in self:
            rec.board = rec.product_id.sub_category.name

    @api.depends('product_id')
    def _compute_color_quality(self):
        for rec in self:
            rec.color_quality = str(rec.product_id.color) + " + " + str(rec.product_id.coating)

    @api.depends('product_id')
    def _compute_impression(self):
        for rec in self:
            if rec.product_id.outs > 0:
                rec.impression = rec.product_qty / rec.product_id.outs
            else:
                rec.impression = 0

    @api.depends('sale_order_id')
    def _compute_hide(self):
        for rec in self:
            if rec.sale_order_id:
                rec.hide = False
            else:
                rec.hide = True

    @api.depends('sale_order_id')
    def _compute_delivery_date(self):
        for rec in self:
            if rec.sale_order_id:
                rec.delivery_date = rec.sale_order_id.commitment_date
            else:
                rec.delivery_date = None

    @api.depends('sale_order_id')
    def _compute_sale_order_partner_id(self):
        for rec in self:
            if rec.sale_order_id:
                rec.sale_order_partner_id = rec.sale_order_id.partner_id.id
            else:
                rec.sale_order_partner_id = ''

    @api.depends('sale_order_id')
    def _compute_sale_order_client_order_ref(self):
        for rec in self:
            if rec.sale_order_id:
                rec.sale_order_client_order_ref = rec.sale_order_id.client_order_ref
            else:
                rec.sale_order_client_order_ref = ''

    @api.depends('sale_order_id')
    def _compute_sale_order_line_id(self):
        for rec in self:
            if rec.sale_order_id:
                values = self.env['sale.order.line'].search([('order_id', '=', self.sale_order_id.ids)])
                for lines in values:
                    if lines.product_id == rec.product_id:
                        rec.sale_order_line_id = lines
                    else:
                        rec.sale_order_line_id = None
            else:
                rec.sale_order_line_id = None

    @api.model
    def _compute_sale_order_id(self):
        for rec in self:
            if rec.origin:
                rec.sale_order_id = self.env['sale.order'].search([('name', '=', rec.origin)])
                print("rec.sale_order_id", rec.sale_order_id)
            else:
                rec.sale_order_id = None
