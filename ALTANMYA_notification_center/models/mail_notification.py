from odoo import _, api, fields, models


class MailNotification(models.Model):
    _inherit = 'mail.notification'
    notification_type = fields.Selection([
        ('inbox', 'Inbox'), ('email', 'Email'),('both', 'both')
         ], string='Notification Type', default='inbox', index=True, required=True)

    _sql_constraints = [
        # email notification: partner is required
        ('notification_partner_required',
         "CHECK(notification_type NOT IN ('email', 'inbox', 'both') OR res_partner_id IS NOT NULL)",
         'Customer is required for inbox / email notification'),
    ]