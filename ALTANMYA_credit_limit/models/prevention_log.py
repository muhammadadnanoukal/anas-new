from odoo import fields, models, api


class PreventionLog(models.Model):
    _name = 'partner.prevention.log'
    _description = 'this model is used to store the sale order / invoice prevention from creation and the reason why'

    partner_id = fields.Many2one('res.partner', string='Customer Name')
    prevention_date = fields.Datetime('Customer Prevention Date')
    so_invoice = fields.Selection([('so', 'Sale Order'), ('invoice', 'Invoice')], string='operation')
    reason = fields.Text('The prevention Reason')
    amount = fields.Float('Total Amount')
