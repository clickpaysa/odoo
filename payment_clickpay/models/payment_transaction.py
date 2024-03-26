# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint
import requests

from werkzeug import urls

from odoo import _, models, fields
from odoo.exceptions import ValidationError

from odoo.addons.payment import utils as payment_utils
from odoo.addons.payment_clickpay.const import TRANSACTION_STATUS_MAPPING
from odoo.addons.payment_clickpay.controllers.main import clickpayController


_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    clickpay_payment_status = fields.Char(_('clickpay Transaction Status'))
    clickpay_payment_id = fields.Char(_('clickpay Payment ID'))
    clickpay_transaction_id = fields.Char(_('clickpay Transaction ID'))
    clickpay_payment_request_id = fields.Char(_('clickpay Payment Request ID'))
    clickpay_payment_amount = fields.Char(_('clickpay Payment Amount'))
    clickpay_payment_currency = fields.Char(_('clickpay Payment Currency'))
    clickpay_refund_id = fields.Char(_('clickpay Refund ID'))
    clickpay_refund_amount = fields.Char(_('clickpay Refunded Amount'))
    clickpay_refund_currency = fields.Char(_('clickpay Refunded Currency'))
    clickpay_refund_createdat = fields.Char(_('clickpay Refunded Date'))
    redirect_url = fields.Char(_('Redirect URL'))

    def _get_specific_rendering_values(self, processing_values):
        """ Override of `payment` to return clickpay-specific rendering values.

        Note: self.ensure_one() from `_get_rendering_values`.

        :param dict processing_values: The generic and specific processing values of the transaction
        :return: The dict of provider-specific processing values.
        :rtype: dict
        """
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'clickpay':
            return res

        # Initiate the payment and retrieve the payment link data.
        # payload = self._get_payment_payload()


        # payment_response = self.provider_id._clickpay_payment_request(
        #     '/payment/request', payload=payload
        # )
        # self.redirect_url = payment_response['redirect_url']
        rendering_values = {
            'api_url': "https://ml.brstdev.com",
        }
        return rendering_values
        # payment_response = self.provider_id._clickpay_payment_request(
        #     '/payment/request', payload=payload
        # )
        # # payment_response = payment_response
        # _logger.info(
        #             "Response payment_response for :\n%s", pprint.pformat(payment_response),
        #         )
        # values = {
        #     'clickpay_payment_request_id': payment_response['tran_ref'],
        # }
        # self.write(values)

        # # Extract the payment link URL and embed it in the redirect form.
        # rendering_values = {
        #     'api_url': payment_response['redirect_url'],
        # }
        # return rendering_values
        
    def _generate_clickpay_payment(self, post_data):
        code = post_data.get('code')
        if code  in ['clickpay',"'clickpay'",'clickpayapplepay',"'clickpayapplepay'",'clickpaymada',"'clickpaymada'",'clickpayamex',"'clickpaymex'",'clickpaycard',"'clickpaycard'",'clickpayapplepayhosted',"'clickpayapplepayhosted'"]:
            return self._generate_request_payload(post_data)
        else:
            return False
        
    def get_profile_id(self, provide_code):
        if provide_code == "clickpay":
            return self.provider_id.clickpay_profile_id
        elif provide_code == "clickpaycard":
            return self.provider_id.clickpaycard_profile_id
        elif provide_code == "clickpaymada":
            return self.provider_id.clickpaymada_profile_id
        elif provide_code == "clickpayamex":
            return self.provider_id.clickpayamex_profile_id
        elif provide_code == "clickpayapplepay":
            return self.provider_id.clickpayapplepay_profile_id
        elif provide_code == 'clickpayapplepayhosted':
            return self.provider_id.clickpayapplepayhosted_profile_id
        else:
            return None  # Or you can return any default value or raise an exception

    def _generate_request_payload(self, post_data):
        reference = post_data.get('reference')
        values = post_data.get('values')
        code = post_data.get('code')
        # base_url = self.provider_id.get_base_url()
        base_url = "https://ml.brstdev.com"
        # base_url 
        # return_url = "https://stack.brstdev.com:5016/payment/click/return"
        return_url = urls.url_join(
            base_url, f'{clickpayController._return_url}'
        )
        # return_url = 'https://stack.brstdev.com/payment/clickpay/return'
        # webhook_url = "https://webhook.site/36c271b9-7650-4691-9012-52296fa37d8e/"
        # callback_url = "https://ml.brstdev.com/payment/clickpay/webhooks"
        callback_url = urls.url_join(
            base_url, f'{clickpayController._callback_url}/{reference}/{code}'
        )  
        # logging.getLogger(self)
        
        partner_id = values.get('partner')
        partner = self.env['res.partner'].sudo().browse(int(partner_id))
        # acquirer_id = self.env['payment.provider'].sudo().browse(int(data.get('acquirer_id')))
        # webhook_url = 'https://9b39-112-196-88-154.ngrok-free.app/payment/clik/webhooks'
        # profile_id = self.get_profile_id(code)
        record = self.env['payment.provider'].sudo().search([('code', '=', code)])
        state_key = record.state
        state_value = 'https://secure.clickpay.com.sa' if state_key == 'test' else 'https://secure.clickpay.com'
        currency_id = values.get('currency')
        currency = self.env['res.currency'].browse(int(currency_id)).name
        profile_id = eval(f"self.env['payment.provider'].sudo().search([['code','=','{code}']]).{code}_profile_id")
        trans_type = eval(f"self.env['payment.provider'].sudo().search([['code','=','{code}']]).{code}_payment_action")
        payload = {
            "profile_id": profile_id,
            "tran_type": trans_type,
            "tran_class": "ecom",
            "cart_id": reference,
            "cart_currency": currency,
            "framed": True,
            "framed_return_top": True,
            "framed_return_parent": True,
            "cart_amount": str(values.get('amount')),
            "cart_description": f"cart_{reference}",
            "return":return_url,
            "callback":callback_url,
            "customer_details": {
                "name": partner.name if partner.name else "",
                "email": partner.email if partner.email else "",
                "phone": partner.phone if partner.phone else "",
                "street1": partner.street if partner.street else "",
                "city": partner.city if partner.city else "",
                "state": partner.state_id.name if partner.state_id.name else "",
                "country": partner.country_id.code if partner.country_id.code else "",
                "zip": partner.zip  if partner.zip else "",
                "ip": "197.220.201.201"
            },
            "shipping_details": {
                "name": partner.name if partner.name else "",
                "email": partner.email if partner.email else "",
                "phone": partner.phone if partner.phone else "",
                "street1": partner.street if partner.street else "",
                "city": partner.city if partner.city else "",
                "state": partner.state_id.name if partner.state_id.name else "",
                "country": partner.country_id.code if partner.country_id.code else "",
                "zip": partner.zip if partner.zip else "0",
                "ip": "197.220.201.201"  # IP can be dynamic or obtained differently
            }
        }
        if code == 'clickpayapplepay' :
            payload.pop('framed')
            payload.pop('framed_return_top')
            payload.pop('framed_return_parent')
        elif code == 'clickpayapplepayhosted':
            payload['paypage_lang'] = 'en'
            payload['framed'] = False
            payload['framed_return_parent'] = False
            payload['framed_return_top'] = True
            payload['payment_methods'] = ['applepay',]
        else: #---- clickpay ---
            payload['cart_currency'] = 'INR'
            payload['return'] = return_url
            # payload['return'] = 'https://ml.brstdev.com/payment/status'
            payload['callback'] = callback_url
        
        return payload

    def _clickpay_main_request(self, endpoint, payload=None, method='POST'):
        url = payload.get('state_value')+endpoint
        server_key = payload.get('server_key')
        payload.pop("state_value")
        payload.pop("server_key")
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            if method == 'GET':
                response = requests.get(url, params=payload, headers=headers, timeout=20)
            else:
                response = requests.post(url, json=payload, headers=headers)
                _logger.info(
                    "Response for %s :\n%s",
                    endpoint, pprint.pformat(response.json()),
                )
                try:
                    response.raise_for_status()
                    return response.json() 
                except requests.exceptions.HTTPError:
                    _logger.exception(
                        "Invalid API request at %s with data:\n%s", url, pprint.pformat(payload),
                    )
                    response_content = response.json()
                    error_code = response_content.get('error')
                    error_message = response_content.get('message')
                    raise ValidationError("clik: " + _(
                        "The communication with the API failed. clik Payment Gateway gave us the following "
                        "information: '%s' (code %s)", error_message, error_code
                    ))
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            _logger.exception("Unable to reach endpoint at %s", url)
            raise ValidationError(
                "clik: " + _("Could not establish the connection to the API.")
            )
            
    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """ Override of `payment` to find the transaction based on clickpay data.

        :param str provider_code: The code of the provider that handled the transaction.
        :param dict notification_data: The notification data sent by the provider.
        :return: The transaction if found.
        :rtype: recordset of `payment.transaction`
        :raise ValidationError: If inconsistent data were received.
        :raise ValidationError: If the data match no transaction.
        """
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if len(tx) == 1:
            return tx

        reference = notification_data.get('cart_id')
        print('reference::',reference)
        if not reference:
            raise ValidationError("clickpay: " + _("Received data with missing reference."))

        tx = self.search([('reference', '=', reference), ('provider_code', '=', provider_code)])
        if not tx:
            raise ValidationError(
                "clickpay: " + _("No transaction found matching reference %s.", reference)
            )
        return tx

    def _process_notification_data(self, notification_data):
        """ Override of `payment` to process the transaction based on clickpay data.

        Note: self.ensure_one() from `_process_notification_data`

        :param dict notification_data: The notification data sent by the provider.
        :return: None
        :raise ValidationError: If inconsistent data were received.
        """
        super()._process_notification_data(notification_data)
        if self.provider_code not in ['clickpay',"'clickpay'",'clickpayapplepay',"'clickpayapplepay'",'clickpaymada',"'clickpaymada'",'clickpayamex',"'clickpaymex'",'clickpaycard',"'clickpaycard'",'clickpayapplepayhosted',"'clickpayapplepayhosted'"]:
            _logger.warning("clickpay: Invalid provider code : %s",self.provider_code)
            return

        payment_id = notification_data.get('tran_ref')
        if not payment_id:
            raise ValidationError("clickpay: " + _("Received data with missing payment id."))
        
        self.clickpay_payment_id = payment_id
        self.clickpay_transaction_id = payment_id
        self.clickpay_payment_status = notification_data.get('status')
        self.clickpay_payment_amount = notification_data.get('cart_amount')
        self.clickpay_payment_currency = notification_data.get('tran_currency')
        self.provider_reference = payment_id
        reference_number = notification_data.get('cart_id')
        payment_status = notification_data.get('status')

        if not payment_status:
            raise ValidationError("clickpay: " + _("Received data with missing status."))

        message = "Payment successful. Transaction Id: "+self.clickpay_payment_id+", "
        message += "Amount Paid: "+self.clickpay_payment_amount

        if payment_status in TRANSACTION_STATUS_MAPPING['pending']:
            self._set_pending(state_message=message)
        elif payment_status in TRANSACTION_STATUS_MAPPING['done']:
            self._set_done(state_message=message)
        elif payment_status in TRANSACTION_STATUS_MAPPING['canceled']:
            self._set_canceled()
        else:  # Classify unsupported payment status as the `error` tx state.
            _logger.warning(
                "clickpay: Received data for transaction with reference %s with invalid payment status: %s",
                reference_number, payment_status
            )
            self._set_error(
                "clickpay: " + _("Received data with invalid status: %s", payment_status)
            )

    def _send_refund_request(self, amount_to_refund=None):
        """ Override of payment to send a refund request to clickpay.

        Note: self.ensure_one()

        :param float amount_to_refund: The amount to refund
        :return: The refund transaction created to process the refund request.
        :rtype: recordset of `payment.transaction`
        """

        self.ensure_one()
        
        refund_tx = super()._send_refund_request(amount_to_refund=amount_to_refund)
        print('refund object : ', refund_tx)
        print('self is ',self)
        print('provider code at refund ',self.provider_code)
        if 'clickpay' not in str(self.provider_code):
            return refund_tx

        # Make the refund request to clickpay
        converted_amount = payment_utils.to_minor_currency_units(
            -refund_tx.amount,  # The amount is negative for refund transactions
            refund_tx.currency_id
        )
        
        headers = {
            'authorization': eval(f"refund_tx.provider_id.{self.provider_code}_server_key"),
            'Content-Type': 'application/json'
        }
        
        cc = refund_tx.currency_id.name
        payload = {
            "profile_id": eval(f"refund_tx.provider_id.{self.provider_code}_profile_id"),
            "tran_type": "refund",
            "tran_class": "ecom",
            "cart_id": refund_tx.reference,
            "cart_currency":cc,
            "cart_amount": str(amount_to_refund),
            "cart_description": "Refund by admin.",
            "tran_ref": self.provider_reference
        }
        print('\n\n Payload used for refund : ',payload,'\n\n')
        response_content = refund_tx.provider_id._clickpay_main_request(
            'https://secure.clickpay.com.sa/payment/request',headers=headers, payload=payload
        )

        _logger.info(
            "clickpay refund request response for transaction with reference %s:\n%s",
            self.reference, pprint.pformat(response_content)
        )

        payment_result = response_content.get('payment_result')
        if payment_result and payment_result.get('response_status') == 'A':
            # Handle the refund request response
            self.clickpay_refund_id = payment_result.get('response_code')
            self.clickpay_refund_createdat = payment_result.get('transaction_time')
            self.clickpay_refund_amount = response_content.get('cart_amount')
            self.clickpay_refund_currency = response_content.get('cart_currency')
            self.provider_reference = self.clickpay_refund_id
            message = "Refund successful. Refund Reference Id: "+self.clickpay_refund_id+", "
            message += "Payment Id: "+self.clickpay_payment_id+", "
            message += "Amount Refunded: "+self.clickpay_refund_amount+", "
            message += "Payment Method: "+response_content.get('payment_info').get('payment_method')+", "
            message += "Created At: "+ self.clickpay_refund_createdat

            self._set_done()
            self.env.ref('payment.cron_post_process_payment_tx')._trigger()

            return refund_tx
        else : 
                raise ValueError('payment not appproved')