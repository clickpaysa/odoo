import logging
import pprint
import json
import hmac
import hashlib


import requests
from werkzeug import urls
from odoo import _, api, fields, models, http
from odoo.exceptions import ValidationError
from odoo.addons.payment_clickpay.const import SUPPORTED_CURRENCIES
from odoo.addons.payment_clickpay.controllers.main import clickpayController


_logger = logging.getLogger(__name__)


class Paymentprovider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[
            ('clickpay', "ClickPay - All"),
            ('clickpaycard', "ClickPay - CreditCard"),
            ('clickpayamex', "ClickPay - Amex"),
            ('clickpaymada', "ClickPay - Mada"),
            ('clickpayapplepay', "ClickPay - ApplePay"),
            ('clickpayapplepayhosted', "ClickPay - Applepay Hosted"),
        ], 
        ondelete={'clickpay': 'set default', 'clickpayapplepay': 'set default', 'clickpaymada': 'set default', 'clickpayamex': 'set default','clickpaycard': 'set default','clickpayapplepayhosted':'set default'}
    )

    @api.model
    def ipn_notification_url(self):
        return urls.url_join(self.env['payment.provider'].sudo().get_base_url(),clickpayController._ipn_notification_url)

    @api.model
    def _get_app_version(self):
        return "1.0"

    app_version = fields.Char(string='App Version', default=_get_app_version, readonly=True)
    # enabled = fields.Boolean(string='Enabled', default=True)
    # title = fields.Char(string='Title')
    clickpay_endpoint_region = fields.Selection([
        ('sa', 'Saudi Arabia'),
        ('other', 'Other')], string='Select Endpoint Region', default='sa',required=True)
    clickpay_profile_id = fields.Char(string='Profile ID')
    clickpay_server_key = fields.Char(string='Server Key')
    clickpay_client_key = fields.Char(string='Client Key')
    clickpay_iframe_mode = fields.Selection([
        ('iframe', 'iFrame'),
        ('redirect', 'Redirect'),
        ('managed_form', 'Managed Form')], string='Redirect', default='redirect',required=True)
    clickpay_allow_ipn_notifications = fields.Boolean(string='Allow IPN Notifications', default=True)
    clickpay_ipn_url = fields.Char(string='IPN URL',default=ipn_notification_url, readonly=True)
    clickpay_hide_shipping_info = fields.Boolean(string='Hide Shipping Info')
    clickpay_payment_action = fields.Selection([
        ('auth', 'Authorize'),
        ('sale', 'Sale')], string='Payment Action', default='sale',required=True)
    clickpay_enable_tokenization = fields.Boolean(string='Enable Tokenization')
    
    # ++++++++++++++++++++++ ClickPay - CreditCard ++++++++++++++++++++++++
    clickpaycard_endpoint_region = fields.Selection([
        ('sa', 'Saudi Arabia'),
        ('other', 'Other')], string='Select Endpoint Region', default='sa',required=True)    
    clickpaycard_profile_id = fields.Char(string='Profile ID')
    clickpaycard_server_key = fields.Char(string='Server Key')
    clickpaycard_client_key = fields.Char(string='Client Key')
    clickpaycard_iframe_mode = fields.Selection([
        ('iframe', 'iFrame'),
        ('redirect', 'Redirect'),
        ('managed_form', 'Managed Form')], string='Redirect', default='redirect',required=True)   
    clickpaycard_allow_ipn_notifications = fields.Boolean(string='Allow IPN Notifications', default=True)
    clickpaycard_ipn_url = fields.Char(string='IPN URL', readonly=True,default=ipn_notification_url)
    clickpaycard_hide_shipping_info = fields.Boolean(string='Hide Shipping Info')
    clickpaycard_payment_action = fields.Selection([
        ('auth', 'Authorize'),
        ('sale', 'Sale')], string='Payment Action', default='sale',required=True)
    clickpaycard_enable_tokenization = fields.Boolean(string='Enable Tokenization')
    # ++++++++++++++++++++++ ClickPay Mada ++++++++++++++++++++++++
    clickpaymada_endpoint_region = fields.Selection([
        ('sa', 'Saudi Arabia'),
        ('other', 'Other')], string='Select Endpoint Region', default='sa',required=True)    
    clickpaymada_profile_id = fields.Char(string='Profile ID')
    clickpaymada_server_key = fields.Char(string='Server Key')
    clickpaymada_client_key = fields.Char(string='Client Key')
    clickpaymada_iframe_mode = fields.Selection([
        ('iframe', 'iFrame'),
        ('redirect', 'Redirect'),
        ('managed_form', 'Managed Form')], string='Redirect', default='redirect',required=True)   
    clickpaymada_allow_ipn_notifications = fields.Boolean(string='Allow IPN Notifications', default=True)
    clickpaymada_ipn_url = fields.Char(string='IPN URL', readonly=True,default=ipn_notification_url)
    clickpaymada_hide_shipping_info = fields.Boolean(string='Hide Shipping Info')
    clickpaymada_payment_action = fields.Selection([
        ('auth', 'Authorize'),
        ('sale', 'Sale')], string='Payment Action', default='sale',required=True)
    clickpaymada_enable_tokenization = fields.Boolean(string='Enable Tokenization')

    # ++++++++++++++++++++++ ClickPay Amex ++++++++++++++++++++++++
    clickpayamex_endpoint_region = fields.Selection([
        ('sa', 'Saudi Arabia'),
        ('other', 'Other')], string='Select Endpoint Region', default='sa',required=True)    
    clickpayamex_profile_id = fields.Char(string='Profile ID')
    clickpayamex_server_key = fields.Char(string='Server Key')
    clickpayamex_client_key = fields.Char(string='Client Key')
    clickpayamex_iframe_mode = fields.Selection([
        ('iframe', 'iFrame'),
        ('redirect', 'Redirect'),
        ('managed_form', 'Managed Form')], string='Redirect', default='redirect',required=True) 
    clickpayamex_allow_ipn_notifications = fields.Boolean(string='Allow IPN Notifications', default=True)
    clickpayamex_ipn_url = fields.Char(string='IPN URL', readonly=True,default=ipn_notification_url)
    clickpayamex_hide_shipping_info = fields.Boolean(string='Hide Shipping Info')
    clickpayamex_payment_action = fields.Selection([
        ('auth', 'Authorize'),
        ('sale', 'Sale')], string='Payment Action', default='sale',required=True)
    clickpayamex_enable_tokenization = fields.Boolean(string='Enable Tokenization')
    
    # ++++++++++++++++++++++ ClickPay ApplePay ++++++++++++++++++++++++
    clickpayapplepay_endpoint_region = fields.Selection([
        ('sa', 'Saudi Arabia'),
        ('other', 'Other')], string='Select Endpoint Region', default='sa',required=True) 

    clickpayapplepay_profile_id = fields.Char(string='Profile ID')
    clickpayapplepay_server_key = fields.Char(string='Server Key')
    clickpayapplepay_client_key = fields.Char(string='Client Key')
    clickpayapplepay_merchantIdentifier = fields.Char(string='Merchant Identifier')
    clickpayapplepay_displayName = fields.Char(string='Display Name')
    clickpayapplepay_initiative = fields.Char(string='Initiative')
    clickpayapplepay_initiativeContext = fields.Char(string='Initiative Context')
    clickpayapplepay_cert_file = fields.Binary(string='Certificate File')
    clickpayapplepay_key_file = fields.Binary(string='Certificate Key File')
    clickpayapplepay_allow_ipn_notifications = fields.Boolean(string='Allow IPN Notifications', default=True)
    clickpayapplepay_ipn_url = fields.Char(string='IPN URL', readonly=True,default=ipn_notification_url)
    clickpayapplepay_hide_shipping_info = fields.Boolean(string='Hide Shipping Info')
    clickpayapplepay_payment_action = fields.Selection([
        ('auth', 'Authorize'),
        ('sale', 'Sale')], string='Payment Action', default='sale',required=True)
    clickpayapplepay_enable_tokenization = fields.Boolean(string='Enable Tokenization')
    # ++++++++++++++++++++++ ClickPay ApplePay HOsted ++++++++++++++++++++++++
    clickpayapplepayhosted_endpoint_region = fields.Selection([
        ('sa', 'Saudi Arabia'),
        ('other', 'Other')], string='Select Endpoint Region', default='sa',required=True) 
    clickpayapplepayhosted_profile_id = fields.Char(string='Profile ID')
    clickpayapplepayhosted_server_key = fields.Char(string='Server Key')
    clickpayapplepayhosted_merchantIdentifier = fields.Char(string='Merchant Identifier')
    clickpayapplepayhosted_displayName = fields.Char(string='Display Name')
    clickpayapplepayhosted_initiative = fields.Char(string='Initiative')
    clickpayapplepayhosted_initiativeContext = fields.Char(string='Initiative Context')
    clickpayapplepayhosted_cert_file = fields.Binary(string='Certificate File')
    clickpayapplepayhosted_key_file = fields.Binary(string='Certificate Key File')
    clickpayapplepayhosted_payment_currency = fields.Selection([
        ('base', 'Base Currency'),
        ('other', 'Other')], string='Payment Currency', default='base',required=True)
    clickpayapplepayhosted_allow_ipn_notifications = fields.Boolean(string='Allow IPN Notifications', default=True)
    clickpayapplepayhosted_ipn_url = fields.Char(string='IPN URL', readonly=True,default=ipn_notification_url)
    clickpayapplepayhosted_hide_shipping_info = fields.Boolean(string='Hide Shipping Info')
    clickpayapplepayhosted_payment_action = fields.Selection([
        ('auth', 'Authorize'),
        ('sale', 'Sale')], string='Payment Action', default='sale',required=True)
    clickpayapplepayhosted_enable_tokenization = fields.Boolean(string='Enable Tokenization')

    def _compute_feature_support_fields(self):
        """ Override of `payment` to enable additional features. """
        super()._compute_feature_support_fields()
        self.update({
            'support_refund': 'partial',
            })  

    
    @api.model   
    def _get_compatible_providers(self, *args, currency_id=None, **kwargs):
        providers = super()._get_compatible_providers(*args, currency_id=currency_id, **kwargs)
        currency = self.env['res.currency'].browse(currency_id).exists()
        if currency:
                for provider_code, supported_currencies in SUPPORTED_CURRENCIES.items():
                    if currency.name not in supported_currencies:
                        providers = providers.filtered(lambda p: p.code != provider_code)
        user_agent = http.request.httprequest.headers.get('User-Agent')
        if not (('iPhone' in user_agent or 'iPad' in user_agent or ('Macintosh' in user_agent and 'Intel Mac OS X' in user_agent)) and 'Safari' in user_agent and 'Chrome' not in user_agent):
            return providers.filtered(lambda p : p.code not in  ['clickpayapplepay','clickpayapplepayhosted'])
        return providers        
    
    
    # @api.model    
    # def _get_supported_currencies(self):
    #     SUPPORTED_CURRENCIESS = ['SAR', 'EUR']
    #     """ Override of `payment` to return the supported currencies. """
    #     supported_currencies = super()._get_supported_currencies()
    #     print(supported_currencies)
    #     if self.code == 'clickpayamex':
    #         supported_currencies = supported_currencies.filtered(
    #             lambda c: c.name in SUPPORTED_CURRENCIESS
    #         )
    #     return supported_currencies 


    def _clickpay_verify_webhook(self, data):
        signing_string = ''
        for k in sorted(data.keys()):
            if k != 'hmac':
                signing_string += str(k)+''+str(data[k])

        signature = hmac.new(
            bytes(self.clik_api_salt, 'utf-8'),
            msg=bytes(signing_string, 'utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()
        return signature
        
    def _clickpay_main_request(self, endpoint,headers, payload=None, main_code=None, method='POST'):

        # self.ensure_one()
        url = endpoint
        try:
            if method == 'GET':
                response = requests.get(url, params=payload, headers=headers, timeout=20)
            else:
                response = requests.post(url, json=payload, headers=headers)

                # response = requests.post(url, data=dict(payload), headers=headers, timeout=20)
                _logger.info(
                    "payload for %s :\n%s",
                    endpoint, pprint.pformat(payload),
                )
                try:
                    response.raise_for_status()
                            
                except requests.exceptions.HTTPError:
                    _logger.exception(
                        "Invalid API request at %s with data:\n%s", url, pprint.pformat(payload),
                    )
                    response_content = response.json()
                    error_code = response_content.get('error')
                    error_message = response_content.get('message')
                    raise ValidationError("clik: " + _(
                        "The communication with the API failed. clik Payment Gateway gave us the following "
                        "information: '%s'", error_message
                    ))
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            _logger.exception("Unable to reach endpoint at %s", url)
            raise ValidationError(
                "clik: " + _("Could not establish the connection to the API.")
            )
        

        return response.json()
    
