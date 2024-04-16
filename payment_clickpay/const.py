TRANSACTION_STATUS_MAPPING = {
    'pending': ('pending'),
    'done': ('completed'),
    'canceled': ('canceled', 'null', 'failed'),
}

SUPPORTED_CURRENCIES = {
    'clickpayamex': {
        'AED',
        'SAR'
        },
    'clickpaymada': {
        'SAR'
        },
    'clickpayapplepay': {
        'AED',
        'SAR'
        },
    'clickpayapplepayhosted':{
        'AED',
        'SAR'
        },
}

DEFAULT_PAYMENT_METHODS_CODES = [
    # Primary payment methods.
    'card',
    # Brand payment methods.
    'visa',
    'mastercard',
    'amex',
    'discover',
]