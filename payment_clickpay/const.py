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
        'SAR',
        },
    'clickpayapplepay': {
        'AED',
        'SAR',
        }       
}

# SUPPORTED_CURRENCIES = {
#     'SAR',
#     'USD',
#     'CAD',
# }