# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Altanmya-Nasr Reports',
    'version': '1.0',
    'sequence': -200,
    'category': 'Inventory/Purchase',
    'depends': ['purchase'],
    'data': [
        'views/purchase_form_view.xml',
        'report/report_info.xml',
        'report/purchase_nasr_report.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
