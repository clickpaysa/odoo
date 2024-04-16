# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging,pprint,json,hashlib,hmac,os

import threading
from werkzeug.exceptions import Forbidden
import requests
from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request
from odoo import _


import base64


_logger = logging.getLogger(__name__)

class clickpayController(http.Controller):
    _iframe_payment = '/payment/clickpay/iframe_payment'
    _return_url = '/payment/clickpay/return'
    _callback_url = '/payment/clickpay/webhooks'
    _ipn_notification_url = '/ipn/notification'
    
    @http.route('/payment/clickpay/applepay/request',methods=['POST'],auth='public',csrf=False)
    def get_payment_cartinfo(self,**post):
        headers = {
            'Content-Type':'application/json',
            'authorization': request.env['payment.provider'].sudo().search([['code','=','clickpayapplepay']]).clickpayapplepay_server_key,
            }
        try:
            url = json.loads(request.httprequest.data).get('url')
            payload = {
                'merchantIdentifier':request.env['payment.provider'].sudo().search([['code','=','clickpayapplepay']]).clickpayapplepay_merchantIdentifier,
                'displayName':request.env['payment.provider'].sudo().search([['code','=','clickpayapplepay']]).clickpayapplepay_displayName,
                'initiative':request.env['payment.provider'].sudo().search([['code','=','clickpayapplepay']]).clickpayapplepay_initiative,
                'initiativeContext':request.env['payment.provider'].sudo().search([['code','=','clickpayapplepay']]).clickpayapplepay_initiativeContext,
            }
            base_dir = os.getcwd()+"/" 
            ssl_cert_path = base_dir+'merchant-cert.cer'
            with open(ssl_cert_path,'w+') as file:
                text = request.env['payment.provider'].sudo().search([['code','=','clickpayapplepay']]).clickpayapplepay_cert_file
                if text is False : raise ValueError('Both files should be added to proceed : (certificate,key)')
                file.write(base64.decodebytes(text).decode())
            cert_key_path = base_dir+'merchant-cert.key'
            with open(cert_key_path,'w+') as file:
                text = request.env['payment.provider'].sudo().search([['code','=','clickpayapplepay']]).clickpayapplepay_key_file
                if text is False : raise ValueError('Both files should be added to proceed : (certificate,key)')
                file.write(base64.decodebytes(text).decode())
            cert =  (ssl_cert_path, cert_key_path)
            response = requests.post(url,headers=headers,json=payload,verify=True,cert=cert)
            return request.make_response(json.dumps(response.json()), headers={'Content-Type': 'application/json'})
        except Exception as e :
            print('error at get_payment_carinfo : ',e)
            response = {'status':False}
            return request.make_response(json.dumps(response),headers={'Content-Type':'application/json'})

    @http.route('/payment/clickpay/applepay/make_payment',methods=['POST'],auth='public',csrf=False)
    def applepay_make_payment(self,**post):
        data = json.loads(request.httprequest.data)
        server_key = request.env['payment.provider'].sudo().search([['code','=','clickpayapplepay']]).clickpayapplepay_server_key
        if not server_key:_logger.exception("Server key must be set for clickpayapplepay");raise ValueError('Server key must be set for clickpayapplepay')
        headers = {'Content-Type':'application/json','Authorization': server_key }
        payload = request.env['payment.transaction'].sudo()._generate_clickpay_payment(data) 
        if not payload: return request.make_response(json.dumps({}),headers={'Content-Type':'application/json'})
        payload['apple_pay_token'] = data.get('payment_token')
        response = requests.post("https://secure.clickpay.com.sa/payment/request",headers=headers,json=payload)
        return request.make_response(json.dumps(response.json()), headers={'Content-Type': 'application/json'})

    @http.route('/payment/clickpay/request',methods=['post','get'],type='http',csrf=False)
    def payment_clickpay_request(self,**data):
        """ Process the notification data sent by clik after redirection from checkout.
        :param dict data: The notification data."""
        url = 'https://secure.clickpay.com.sa/payment/request'
        headers = {
                'authorization': eval(f"request.env['payment.provider'].search([['code','=','{data.get('code')}']]).{data.get('code')}_server_key"),
                'Content-Type': 'application/json',
                'Accept':'application/json'
            }
        cookies = {'session_id':request.httprequest.cookies.get('session_id')}
        data['values'] = {'partner':data.get('partner'),'currency':data.get('currency'),'amount':data.get('amount')}
        req_json = request.env['payment.transaction'].sudo()._generate_clickpay_payment(data)
        req_json['payment_token'] = data.get('token')
        try:
            response = requests.post(url,data=json.dumps(req_json),headers=headers,cookies=cookies)
            if response.json().get('redirect_url') is not None:return request.redirect(response.json().get('redirect_url'))
        except Exception as e:
            print('payment_clickpay_request : ',e)
        return request.redirect('/payment/status')

    @http.route('/ipn/notification',auth='public')
    def handler_ipn_notification(self,**data):
        print(data)
        return 'ok'

    @http.route(_iframe_payment, type='json', auth='public')
    def handle_iframe_orders_from_checkout(self, **post):
        code = post.get('code')
        if code == 'clickpayapplepayhosted':
            try:
                required_fields = ['profile_id','server_key','merchantIdentifier','displayName','initiative','initiativeContext','cert_file']
                for field in required_fields:
                    value = eval(f"request.env['payment.provider'].sudo().search([['code','=','clickpayapplepayhosted']]).clickpayapplepayhosted_{field}")
                    if not value: raise ValueError((field)+' is requeried to accept payments with applepayhosted .')
                payload = request.env['payment.transaction'].sudo()._generate_clickpay_payment(post)
                url = 'https://secure.clickpay.com.sa/payment/request'
                server_key = request.env['payment.provider'].sudo().search([['code','=','clickpayapplepayhosted']]).clickpayapplepayhosted_server_key
                headers = {'Content-Type':'applicationn/json','authorization':server_key}
                response_ = requests.post(url=url,json=payload,headers=headers)
                return response_.json()
            except Exception as e :
                print('handle_iframe_orders_from_checkout : ',e)
                return {'status':False,'details':str(e)}
        elif code == 'clickpayapplepay':
            response = {'status':False}
            try:
                required_fields = ['profile_id','server_key','client_key','merchantIdentifier','displayName','initiative','initiativeContext','cert_file','key_file']
                for field in required_fields:
                    value = eval(f"request.env['payment.provider'].sudo().search([['code','=','clickpayapplepay']]).clickpayapplepay_{field}")
                    if not value: raise ValueError((field)+' is requeried to accept payments with applepay .')
                payload = request.env['payment.transaction'].sudo()._generate_clickpay_payment(post) 
                cart_currency = str(payload.get('cart_currency')) 
                amount = str(payload.get('cart_amount')) 
                name = payload.get('customer_details').get('name')
                country = payload.get('customer_details').get('country')
                response['data'] = {
                    'data': {
                        'countryCode':country,
                        'currencyCode':cart_currency,
                        'merchantCapabilities':['supports3DS'],
                        'supportedNetworks':['visa','mada','masterCard','amex'],
                        'total':{'label':f'Click Pay {name}','type':'final','amount':amount},
                    }
                }
                response['status'] = True
            except Exception as e:
                print('handle_iframe_orders_from_checkout : ',e)
                response['details'] = str(e)
            return response
        payment_provider = request.env['payment.provider'].sudo().search([('code', '=', code)], limit=1)
        if payment_provider:
            try:
                payment_mode_key = code + '_iframe_mode'
                _client_key = code + '_client_key'
                if hasattr(payment_provider, payment_mode_key):
                    payment_mode = getattr(payment_provider, payment_mode_key)
                    _id = getattr(payment_provider, _client_key)
                    if payment_mode == "managed_form":
                        response = { 
                                'data': _id,
                                'status': True, 
                                'type': payment_mode }    
                        return response
                    else:
                        payload = request.env['payment.transaction'].sudo()._generate_clickpay_payment(post) 
                        payment_response = self._clickpay_main_api_request('/payment/request', payload, code) 
                        if payment_response:
                            _logger.info(
                                "Response for %s :\n%s",
                                'url', pprint.pformat(payment_response),
                            )
                            response = {
                                'data': payment_response,
                                'status': True, 
                                'type': payment_mode
                            }    
                            return response
                        else:
                            response = {
                                'data': False,
                                'status': False, 
                                'type': False,
                                'error_message': 'Something Went Wrong!!'
                            }    
                            return response
                        
                else:
                    response = {
                        'data': False,
                        'status': False, 
                        'type': False,
                        'error_message': 'Something Went Wrong!!'
                    }    
                    return response
            except Exception as e: 
                _logger.exception("Error while processing ClickPay payment request: %s", str(e))
                return {'status': False, 'error_message': 'Error processing payment request'}
        else:
            return {'status': False, 'error_message': 'Payment provider not found'}

    
    @http.route(_return_url, type='http', auth='public', csrf=False,save_session=False)
    def clik_return_from_checkout(self, **data):
        """ Process the notification data sent by clik after redirection from checkout.
        :param dict data: The notification data.
        """
        if data.get('respStatus') == 'A':
            return request.redirect('/payment/status')
        else:
            return request.redirect('/shop/payment')

    
    @http.route(f'{_callback_url}/<reference>/<code>', type='json',auth='public',methods=['POST'], csrf=False,website=True)
    def clickpay_webhook(self, reference, code, **data):
        headers = request.httprequest.headers
        signature = headers.get('signature')
        data = json.loads(request.httprequest.data)
        body = request.httprequest.data
        server_key =  eval(f"request.env['payment.provider'].sudo().search([['code','=','{code}']]).{code}_server_key")
        _logger.info("Callback received from payment gateway with data:\n%s", pprint.pformat(data))
        _logger.info("Callback received from payment gateway with code:\n%s", pprint.pformat(code))
        try:
            payment_result = data.get('payment_result')
            print('payment result : ',payment_result)
            if payment_result.get('response_status') == 'A':data['status'] = 'completed' 
            elif payment_result.get('response_status') == 'C':data['status'] = 'canceled'
            else: data['status'] = 'failed'
            tx_sudo = request.env['payment.transaction'].sudo()._get_tx_from_notification_data(code, data)
            self.verify_signature(body,signature,server_key)
            tx_sudo._handle_notification_data(code, data)
        except Exception as e:
            _logger.exception("An error occurred while processing webhook: %s", str(e))
        return 'Ok'


    @staticmethod
    def verify_signature(body, signature, server_key):
        """
        Verify the signature using HMAC-SHA256 hashing algorithm.
        """
        calculated_signature = hmac.new(server_key.encode(), body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(calculated_signature, signature) :
            _logger.warning("ClickPay:Received notification with invalid signature.")
            raise Forbidden()
        
    def _clickpay_main_api_request(self, endpoint, payload=None, main_code=None, method='POST'):
        record = request.env['payment.provider'].sudo().search([('code', '=', main_code)])
        ApiURL = 'https://secure.clickpay.com.sa'
        url = ApiURL+endpoint
        
        profile_id_key = main_code + '_profile_id'
        server_key_key = main_code + '_server_key'
        _payment_action = main_code + '_payment_action'
        _hide_shipping_info = main_code + '_hide_shipping_info'
        _enable_tokenization = main_code + '_enable_tokenization'
        if hasattr(record, server_key_key):
            server_key = getattr(record, server_key_key)
            profile_id = getattr(record, profile_id_key)
            payment_action = getattr(record, _payment_action)
            enable_tokenization = getattr(record, _enable_tokenization)
            hide_shipping_info = getattr(record, _hide_shipping_info)
            if enable_tokenization:
                payload['tokenise'] = '2'
            if hide_shipping_info:
                payload['hide_shipping'] = True
            payload['profile_id'] = profile_id
            payload['tran_type'] = payment_action
            headers = {
                'authorization': server_key,
                'Content-Type': 'application/json'
            }
            cookies = {"session_id":request.httprequest.cookies.get('session_id')}
            try:
                if method == 'GET':
                    response = requests.get(url, params=payload, headers=headers, timeout=20)
                else:
                    response = requests.post(url, json=payload, headers=headers,cookies=cookies)
                    _logger.info(
                        "payload for %s :\n%s",
                        main_code, pprint.pformat(payload),
                    )
                    try:
                        response.raise_for_status()
                        return response.json() 
                                
                    except requests.exceptions.HTTPError:
                        _logger.exception("Invalid API request at %s with data:\n%s", url, pprint.pformat(payload))
                        response_content = response.json()
                        error_code = response_content.get('error')
                        error_message = response_content.get('message')
                        raise ValidationError("clickpay: " + _("The communication with the API failed. clickpay Payment Gateway gave us the following "
                            "information: '%s' (code %s)", error_message, error_code))                    
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                _logger.exception("Unable to reach endpoint at %s", url)
                raise ValidationError("clickpay: " + _("Could not establish the connection to the API."))    
        else:
            
            return False

