from odoo import api, fields, models, _
from odoo.exceptions import UserError
import datetime


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model_create_multi
    def create(self, vals_list):
        record = super().create(vals_list)
        partner = record.partner_id.commercial_partner_id
        record.compute_partner_late_payment()
        save = False
        try:
            if partner.c_use_partner_credit_limit:
                print(partner.c_credit_limit, partner.credit, record.amount_total)
                if partner.c_credit_limit < partner.credit + record.amount_total:
                    if partner.action_type == 'nothing':
                        pass
                    elif partner.action_type == 'block':
                        save = True
                        raise UserError(
                            f'{partner.name} has reached its Credit Limit of : {partner.c_credit_limit}')
        finally:
            print('fina 1', save)
            if save:
                amount_total = record.amount_total
                self.env.cr.rollback()
                self.create_prevention_log_rec(partner,
                                               'the customer has reached his Credit Limit', amount_total)

        try:
            if record.compute_partner_late_payment():
                if partner.action_type == 'nothing':
                    pass
                elif partner.action_type == 'block':
                    save = True
                    raise UserError(
                        f'{partner.name} has unpaid invoices and the payment deadline is over')
        finally:
            print('fina 2', save)
            if save:
                amount_total = record.amount_total
                self.env.cr.rollback()
                self.create_prevention_log_rec(partner,
                                               'the customer has unpaid invoices and the payment deadline is over',
                                               amount_total)
        print('order record : ', record)
        return record

    def write(self, vals):
        order = super().write(vals)
        print('so vals in cre lim : ', vals, order, self.partner_id)
        partner_id = vals.get('partner_id') if vals.get('partner_id') is not None else self.partner_id
        print('type : ', type(partner_id))
        if type(partner_id) == type(self.id):
            partner_id = self.env['res.partner'].search([('id', '=', partner_id)])
        amount_total = vals.get('amount_total') if vals.get('amount_total') is not None else self.amount_total
        print('man I\'m bored ', partner_id, amount_total)
        partner = partner_id.commercial_partner_id
        # self.compute_partner_late_payment()
        if partner.c_use_partner_credit_limit:
            print(partner.c_credit_limit, partner.credit, amount_total)
            if partner.c_credit_limit < partner.credit + amount_total:
                if partner.action_type == 'nothing':
                    pass
                elif partner.action_type == 'block':
                    self.create_prevention_log_rec(partner,
                                                   'the customer has reached his Credit Limit', self.amount_total)
                    raise UserError(
                        f'{partner.name} has reached its Credit Limit of : {partner.c_credit_limit}')
        # if self.compute_partner_late_payment():
        #     if partner.action_type == 'nothing':
        #         pass
        #     elif partner.action_type == 'block':
        #         self.create_prevention_log_rec(partner,
        #                                        'the customer has unpaid invoices and the payment deadline is over')
        #         raise UserError(
        #             f'{partner.name} has unpaid invoices and the payment deadline is over')
        return order

    def compute_partner_late_payment(self):
        order_id = self.id if self.id else -1
        late_invoices = self.env['account.move'].search(
            [('partner_id', '=', self.partner_id.id),
             ('invoice_date_due', '<', fields.Datetime.now() - datetime.timedelta(
                 days=self.partner_id.commercial_partner_id.number_of_allowed_late_days)),
             ('state', '=', 'posted'), ('id', '!=', order_id)])
        print('late invoices : ', late_invoices)
        if len(late_invoices) >= 1:
            return True
        else:
            return False

    @api.depends('company_id', 'partner_id', 'amount_total')
    def _compute_partner_credit_warning(self):
        for order in self:
            order.with_company(order.company_id)
            order.partner_credit_warning = ''
            show_warning = order.state in ('draft', 'sent') and \
                           order.company_id.account_use_credit_limit
            if self.partner_id.action_type == 'warning':
                updated_credit = order.partner_id.commercial_partner_id.credit + (
                        order.amount_total * order.currency_rate)
                order.partner_credit_warning = self.env['account.move']._build_credit_warning_message(
                    order, updated_credit)

    def create_prevention_log_rec(self, partner, reason, amount):
        print('re', reason)
        rec = self.env['partner.prevention.log'].sudo().create({
            'partner_id': partner.id,
            'prevention_date': fields.Datetime.now(),
            'so_invoice': 'so',
            'reason': reason,
            'amount': amount
        })
        self.env.cr.commit()
        print('rec : ', rec)
