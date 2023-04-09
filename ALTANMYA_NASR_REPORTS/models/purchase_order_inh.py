# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _
import base64
from num2words import num2words



class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    Attention = fields.Char('Attention')
    Remarks = fields.Html('Remarks')
    Type = fields.Char('Type')

    Via = fields.Char('Via')
    ETA = fields.Char('ETA')
    SN = fields.Integer('SN')


    Payment_Method = fields.Char('Payment Method')

    qty = fields.Char('Qty', compute='_get_Qty', store=True)

    Total_quantity_ordered = fields.Char('Total_quantity_ordered ', compute='_get_value', store=True)
    total_format = fields.Char('total_format', compute='_get_value', store=True)

    Date_print = fields.Datetime("date", compute='_get_value', store=True)

    total_price_words = fields.Char('Total Price in Words', compute='_get_value')

    @api.depends('order_line.product_qty', 'order_line.product_uom_qty')
    def _get_Qty(self):
        for rec in self:
            mm = self.env['purchase.order.line'].search([('order_id', '=', rec.id)])
            for qtt in mm:
                rec.qty = str(qtt.product_qty) + " " + qtt.product_uom.name
            print(" rec.qty", rec.qty)

    @api.depends('order_line.product_qty', 'order_line.product_uom_qty')
    def _get_value(self):
        for order in self:
            qty = 0
            for line in order.order_line:
                qty += line.product_qty
            order.Total_quantity_ordered = str(qty)
            currency_symbol = order.currency_id.symbol or ''
            total_price_words = num2words(float(order.amount_total)).title()
            order.total_price_words = f"{total_price_words} {currency_symbol}"
            # order.total_price_words = currency and num2words(amount, to='currency', lang='en',
            #                                                  currency=currency.name).title() or ''
            # order.total_price_words = num2words(float(order.amount_total)).title()
            print('vv order.total_price_words vv', order.total_price_words)
            print("rder.Total_quantity_ordered", order.Total_quantity_ordered)


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    sequence_ref = fields.Integer('No.', compute="_sequence_ref")

    # def _prepare_stock_moves(self, picking):
    #     self.ensure_one()
    #     res = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)
    #     for val in res:
    #         if val.get('product_id') == self.product_id.id:
    #             val.update({'sequence_ref': self.sequence_ref})
    #     return res

    @api.depends('order_id.order_line', 'order_id.order_line.product_id')
    def _sequence_ref(self):
        for line in self:
            no = 0
            line.sequence_ref = no
            for l in line.order_id.order_line:
                no += 1
                l.sequence_ref = no
