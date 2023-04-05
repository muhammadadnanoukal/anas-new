from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.fields import Command
from odoo.exceptions import AccessError
from itertools import groupby


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    show_retention = fields.Boolean('Show Retention Rate?')
    retention_rate = fields.Float('Retention Rate')
    retention_amount = fields.Float('Retention Amount', compute='compute_retention_amount')
    total_without_retention = fields.Float('Total Without Retention', compute='compute_total_without_retention')

    @api.depends('retention_rate', 'amount_untaxed')
    def compute_retention_amount(self):
        for rec in self:
            rec.retention_amount = rec.retention_rate * rec.amount_untaxed

    @api.depends('retention_rate', 'amount_untaxed')
    def compute_total_without_retention(self):
        for rec in self:
            rec.total_without_retention = rec.amount_untaxed - rec.retention_amount

    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sales order. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
        self.ensure_one()

        invoice_vals = {
            'ref': self.client_order_ref or '',
            'move_type': 'out_invoice',
            'narration': self.note,
            'currency_id': self.currency_id.id,
            'campaign_id': self.campaign_id.id,
            'medium_id': self.medium_id.id,
            'source_id': self.source_id.id,
            'team_id': self.team_id.id,
            'partner_id': self.partner_invoice_id.id,
            'partner_shipping_id': self.partner_shipping_id.id,
            'fiscal_position_id': (self.fiscal_position_id or self.fiscal_position_id._get_fiscal_position(self.partner_invoice_id)).id,
            'invoice_origin': self.name,
            'invoice_payment_term_id': self.payment_term_id.id,
            'invoice_user_id': self.user_id.id,
            'payment_reference': self.reference,
            'transaction_ids': [Command.set(self.transaction_ids.ids)],
            'company_id': self.company_id.id,
            'invoice_line_ids': [],
        }
        if self.show_retention:
            invoice_vals['show_retention'] = self.show_retention
            invoice_vals['retention_rate'] = self.retention_rate

        return invoice_vals

    # def _create_invoices(self, grouped=False, final=False, date=None):
    #     """ Create invoice(s) for the given Sales Order(s).
    #
    #     :param bool grouped: if True, invoices are grouped by SO id.
    #         If False, invoices are grouped by keys returned by :meth:`_get_invoice_grouping_keys`
    #     :param bool final: if True, refunds will be generated if necessary
    #     :param date: unused parameter
    #     :returns: created invoices
    #     :rtype: `account.move` recordset
    #     :raises: UserError if one of the orders has no invoiceable lines.
    #     """
    #     if not self.env['account.move'].check_access_rights('create', False):
    #         try:
    #             self.check_access_rights('write')
    #             self.check_access_rule('write')
    #         except AccessError:
    #             return self.env['account.move']
    #
    #     # 1) Create invoices.
    #     invoice_vals_list = []
    #     invoice_item_sequence = 0  # Incremental sequencing to keep the lines order on the invoice.
    #     for order in self:
    #         order = order.with_company(order.company_id)
    #         print('order', order)
    #
    #         invoice_vals = order._prepare_invoice()
    #         print('invoice vals', invoice_vals)
    #         print('show rate ? ', order.show_retention)
    #         if order.show_retention:
    #             invoice_vals['show_retention'] = order.show_retention
    #             invoice_vals['retention_rate'] = order.retention_rate
    #
    #         invoiceable_lines = order._get_invoiceable_lines(final)
    #
    #         if not any(not line.display_type for line in invoiceable_lines):
    #             continue
    #
    #         invoice_line_vals = []
    #
    #         down_payment_section_added = False
    #         for line in invoiceable_lines:
    #             if not down_payment_section_added and line.is_downpayment:
    #                 # Create a dedicated section for the down payments
    #                 # (put at the end of the invoiceable_lines)
    #                 invoice_line_vals.append(
    #                     Command.create(
    #                         order._prepare_down_payment_section_line(sequence=invoice_item_sequence)
    #                     ),
    #                 )
    #                 down_payment_section_added = True
    #                 invoice_item_sequence += 1
    #             invoice_line_vals.append(
    #                 Command.create(
    #                     line._prepare_invoice_line(sequence=invoice_item_sequence)
    #                 ),
    #             )
    #             invoice_item_sequence += 1
    #
    #         invoice_vals['invoice_line_ids'] += invoice_line_vals
    #         invoice_vals_list.append(invoice_vals)
    #
    #     if not invoice_vals_list and self._context.get('raise_if_nothing_to_invoice', True):
    #         raise UserError(self._nothing_to_invoice_error_message())
    #
    #     # 2) Manage 'grouped' parameter: group by (partner_id, currency_id).
    #     if not grouped:
    #         new_invoice_vals_list = []
    #         invoice_grouping_keys = self._get_invoice_grouping_keys()
    #         invoice_vals_list = sorted(
    #             invoice_vals_list,
    #             key=lambda x: [
    #                 x.get(grouping_key) for grouping_key in invoice_grouping_keys
    #             ]
    #         )
    #         for _grouping_keys, invoices in groupby(invoice_vals_list,
    #                                                 key=lambda x: [x.get(grouping_key) for grouping_key in
    #                                                                invoice_grouping_keys]):
    #             origins = set()
    #             payment_refs = set()
    #             refs = set()
    #             ref_invoice_vals = None
    #             for invoice_vals in invoices:
    #                 if not ref_invoice_vals:
    #                     ref_invoice_vals = invoice_vals
    #                 else:
    #                     ref_invoice_vals['invoice_line_ids'] += invoice_vals['invoice_line_ids']
    #                 origins.add(invoice_vals['invoice_origin'])
    #                 payment_refs.add(invoice_vals['payment_reference'])
    #                 refs.add(invoice_vals['ref'])
    #             ref_invoice_vals.update({
    #                 'ref': ', '.join(refs)[:2000],
    #                 'invoice_origin': ', '.join(origins),
    #                 'payment_reference': len(payment_refs) == 1 and payment_refs.pop() or False,
    #             })
    #             new_invoice_vals_list.append(ref_invoice_vals)
    #         print('invoice vals list', new_invoice_vals_list)
    #         invoice_vals_list = new_invoice_vals_list
    #
    #     # 3) Create invoices.
    #
    #     # As part of the invoice creation, we make sure the sequence of multiple SO do not interfere
    #     # in a single invoice. Example:
    #     # SO 1:
    #     # - Section A (sequence: 10)
    #     # - Product A (sequence: 11)
    #     # SO 2:
    #     # - Section B (sequence: 10)
    #     # - Product B (sequence: 11)
    #     #
    #     # If SO 1 & 2 are grouped in the same invoice, the result will be:
    #     # - Section A (sequence: 10)
    #     # - Section B (sequence: 10)
    #     # - Product A (sequence: 11)
    #     # - Product B (sequence: 11)
    #     #
    #     # Resequencing should be safe, however we resequence only if there are less invoices than
    #     # orders, meaning a grouping might have been done. This could also mean that only a part
    #     # of the selected SO are invoiceable, but resequencing in this case shouldn't be an issue.
    #     if len(invoice_vals_list) < len(self):
    #         SaleOrderLine = self.env['sale.order.line']
    #         for invoice in invoice_vals_list:
    #             sequence = 1
    #             for line in invoice['invoice_line_ids']:
    #                 line[2]['sequence'] = SaleOrderLine._get_invoice_line_sequence(new=sequence,
    #                                                                                old=line[2]['sequence'])
    #                 sequence += 1
    #
    #     # Manage the creation of invoices in sudo because a salesperson must be able to generate an invoice from a
    #     # sale order without "billing" access rights. However, he should not be able to create an invoice from scratch.
    #     moves = self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(invoice_vals_list)
    #
    #     # 4) Some moves might actually be refunds: convert them if the total amount is negative
    #     # We do this after the moves have been created since we need taxes, etc. to know if the total
    #     # is actually negative or not
    #     if final:
    #         moves.sudo().filtered(lambda m: m.amount_total < 0).action_switch_invoice_into_refund_credit_note()
    #     for move in moves:
    #         move.message_post_with_view(
    #             'mail.message_origin_link',
    #             values={'self': move, 'origin': move.line_ids.sale_line_ids.order_id},
    #             subtype_id=self.env['ir.model.data']._xmlid_to_res_id('mail.mt_note'))
    #     return moves
