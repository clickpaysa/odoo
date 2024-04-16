from . import controllers
from . import models


from odoo.addons.payment import setup_provider, reset_payment_provider


def post_init_hook(env):
    setup_provider(env, 'clickpay')
    setup_provider(env, 'clickpaycard')
    setup_provider(env, 'clickpayamex')
    setup_provider(env, 'clickpaymada')
    setup_provider(env, 'clickpayapplepay')
    setup_provider(env, 'clickpayapplepayhosted')


def uninstall_hook(env):
    reset_payment_provider(env, 'clickpay')
    reset_payment_provider(env, 'clickpaycard')
    reset_payment_provider(env, 'clickpayamex')
    reset_payment_provider(env, 'clickpaymada')
    reset_payment_provider(env, 'clickpayapplepay')
    reset_payment_provider(env, 'clickpayapplepayhosted')