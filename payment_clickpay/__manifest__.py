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
        'views/payment_clik_templates.xml',
        'views/payment_provider_views.xml',
		'data/payment_icon_data.xml',
        'data/payment_provider_data.xml',
    ],
    'images': ['images/main_screenshot.png'],
    'application': True,
    'installable': True,
}
