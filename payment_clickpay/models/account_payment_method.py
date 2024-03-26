# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class AccountPaymentMethod(models.Model):
    _inherit = 'account.payment.method'

    @api.model
    def _get_payment_method_information(self):
        res = super()._get_payment_method_information()
        res['clickpay'] = {'mode': 'unique', 'domain': [('type', '=', 'bank')]}
        res['clickpaycard'] = {'mode': 'unique', 'domain': [('type', '=', 'bank')]}
        res['clickpayapplepay'] = {'mode': 'unique', 'domain': [('type', '=', 'bank')]}
        res['clickpaymada'] = {'mode': 'unique', 'domain': [('type', '=', 'bank')]}
        res['clickpayamex'] = {'mode': 'unique', 'domain': [('type', '=', 'bank')]}
        return res