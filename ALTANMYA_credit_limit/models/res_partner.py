from odoo import models, fields


class Partner(models.Model):
    _inherit = "res.partner"

    c_credit_limit = fields.Float(
        string='Customer Credit Limit', help='Credit limit specific to this partner.')
    c_use_partner_credit_limit = fields.Boolean(string='Partner Limit ?')
    action_type = fields.Selection(
        [('nothing', 'Do Nothing'), ('warning', 'Warning'), ('block', 'Prevent The Create Operation')],
        string='Action to execute when Exceeding the credit limit or the customer has amount due', default='nothing')
    number_of_allowed_late_days = fields.Integer('Number Of Allowed Days After Due Date')
