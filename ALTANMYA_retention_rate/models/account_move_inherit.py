from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

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
