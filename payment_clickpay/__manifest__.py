{
    'name': "ClickPay Payment Gateway",
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'sequence': 350,
    'summary': "Clickpay Payment Gateway Plugin allows merchants to accept Payments.",
    'author': 'TechSupport',
    'website': 'https://www.clickpay.com.sa',
    'depends': ['payment'],
    'assets': {
        'web.assets_frontend': [
            'payment_clickpay/static/src/js/payment_form.js',
        ],
    },
    'data': [
        'views/payment_click_templates.xml',
        'views/payment_provider_views.xml',
        'data/payment_provider_data.xml',
    ],
    'post_init_hook':'post_init_hook',
    'uninstall_hook':'uninstall_hook',
    'images': ['images/main_screenshot.png'],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}