from odoo import api, fields, models, _


class StockPickingNasr(models.Model):
    _inherit = 'stock.picking'

    random_unique_number = fields.Char(string='Random Unique Number', compute='_compute_random_unique_number')
    partial_delivery = fields.Char(string='Partial Delivery', compute='_compute_partial_delivery')

    @api.depends('backorder_id')
    def _compute_partial_delivery(self):
        for rec in self:
            rec.partial_delivery = '001'
            counter = 1
            found_backorders = rec.env['stock.picking'].search([('origin', '=', rec.origin)])
            if found_backorders:
                for back_orders in found_backorders:
                    if rec.backorder_id:
                        sale_order_id = rec.env['sale.order'].search([('name', '=', back_orders.origin)])
                        if rec.id > back_orders.id:
                            if sale_order_id:
                                counter += 1
                if len(str(counter)) == 1:
                    rec.partial_delivery = '00' + str(counter)
                if len(str(counter)) == 2:
                    rec.partial_delivery = '0' + str(counter)
                if len(str(counter)) == 3:
                    rec.partial_delivery = str(counter)

    def _compute_random_unique_number(self):
        for rec in self:
            rec.random_unique_number = 1137356748381521741 + rec.id
            rec.random_unique_number = '(00)' + rec.random_unique_number[-17:]
