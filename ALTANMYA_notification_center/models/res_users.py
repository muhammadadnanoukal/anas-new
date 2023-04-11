from odoo import _, api, exceptions, fields, models, modules, tools


class Users(models.Model):
    _name = 'res.users'
    _inherit = ['res.users']
    notification_type = fields.Selection([
        ('email', 'Handle by Emails'),
        ('inbox', 'Handle in Odoo'),
        ('both', 'Handle by both')
    ],
        'Notification', required=True, default='email',
        help="Policy on how to handle Chatter notifications:\n"
             "- Handle by Emails: notifications are sent to your email address\n"
             "- Handle in Odoo: notifications appear in your Odoo Inbox")
