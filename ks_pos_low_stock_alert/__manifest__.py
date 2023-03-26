# -*- coding: utf-8 -*-
{
    'name': "POS Low Stock Alert",
    'summary': """""",
    'description': """ """,
    'author': 'Ksolves India Ltd.',
    'website': "https://store.ksolves.com/",
    'category': 'Point Of Sale',
    'version': '15.0.1.0.1',
    'images': ['static/description/pos_15.jpg'],
    'depends': ['base', 'base_setup', 'point_of_sale'],
    'data': ['views/config.xml'],
    'assets' : {
        'point_of_sale.assets': [
            'ks_pos_low_stock_alert/static/src/css/ks_low_stock.css',
            'ks_pos_low_stock_alert/static/src/js/ks_utils.js',
            'ks_pos_low_stock_alert/static/src/js/ks_low_stock.js',
            'ks_pos_low_stock_alert/static/src/js/ks_product_list.js',
            'ks_pos_low_stock_alert/static/src/js/ks_product_screen.js',
            'ks_pos_low_stock_alert/static/src/js/ks_product_widget.js',
        ],
        'web.assets_qweb': [
            'ks_pos_low_stock_alert/static/src/xml/**/*',
        ]
    }
}
