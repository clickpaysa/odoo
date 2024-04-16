/** @odoo-module */

import { _t } from '@web/core/l10n/translation';
import checkoutForm from '@payment/js/payment_form';
import manageForm from '@payment/js/payment_form';


$(document).on("input", "#cardnumber", function () {
    var cardNumber = $(this).val();
    var cardNumber = $(this).val().replace(/\s/g, "");
    var cardType = getCardType(cardNumber);
    $(".ccicon").hide();
    // var code_ele = document.getElementById("code-input");
    // var btn = document.getElementById("manage-form-submit-button");
    // if (code_ele.value == "clickpayamex" && cardType == "amex"){
    //     btn.style.opacity = 1;
    //     btn.removeAttribute("disabled");
    // }else if (code_ele.value == "clickpaymada" && cardType == "mada"){
    //     btn.style.opacity = 1 ; 
    //     btn.removeAttribute("disabled");
    // }else{
    //     btn.setAttribute("disabled","disabled");
    //     btn.style.opacity = 0.6;
    // };
    if (cardType) {
        $(".ccicon").show();
        $(".ccicon").attr("src", "/payment_clickpay/static/description/" + cardType + ".png");
    } else {
        $(".ccicon").attr("src", "");
    }
});
var apple_pay_request;
var cart_data;
var applepay_button_element = document.getElementById('applepaybutton');
if (applepay_button_element != null) {
    applepay_button_element.addEventListener('click', (e) => {
        if (!ApplePaySession) {
            _show_log("ApplePay Session not found");
            return;
        };
        const request = apple_pay_request;
        const session = new ApplePaySession(14, request);
        session.onvalidatemerchant = async event => {
            fetch('/payment/clickpay/applepay/request', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ 'url': event.validationURL }) })
                .then(res => res.json())
                .then(merchantSession => {
                    session.completeMerchantValidation(merchantSession);
                    _show_log("on validate merchant complete");
                })
                .catch(err => {
                    _show_log("Error fetching merchant session", err);
                });
            _show_log("on validate merchant waiting");
        };

        session.onpaymentmethodselected = event => {
            _show_log("on payment method selected begin");
            // Define ApplePayPaymentMethodUpdate based on the selected payment method.
            // No updates or errors are needed, pass an empty object.
            const update = {
                "newTotal": {
                    'label': request['total']['label'],
                    'type': 'final',
                    'amount': request['total']['amount']
                }
            };
            session.completePaymentMethodSelection(update);
            _show_log("on paymentmethod selected complete");
        };

        session.onshippingmethodselected = event => {
            _show_log("on shippingmethod selected begin");
            // Define ApplePayShippingMethodUpdate based on the selected shipping method.
            // No updates or errors are needed, pass an empty object. 
            const update = {};
            session.completeShippingMethodSelection(update);
            _show_log("on shipping method selected complete");
        };

        session.onshippingcontactselected = event => {
            _show_log("on shipping contact selected begin");
            // Define ApplePayShippingContactUpdate based on the selected shipping contact.
            const update = {};
            session.completeShippingContactSelection(update);
            _show_log("on shipping contact selected complete");
        };

        session.onpaymentauthorized = event => {
            _show_log("on payment authorized begin");
            let paymentToken = event.payment.token;
            cart_data['payment_token'] = paymentToken;
            fetch("/payment/clickpay/applepay/make_payment", {
                method: "POST",
                headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                body: JSON.stringify(cart_data),
            })
                .then(res => res.json())
                .then(res => {
                    console.log(res);
                    if (res.payment_result.response_status == 'A'){
                        session.completePayment(0);
                        setTimeout(() => { window.location.href = '/payment/status' }, 2000);
                        window.location.href = '/payment/status';
                    }else{
                        session.completePayment(1);
                    }
                    _show_log("on payment authorized complete");
                })
                .catch(err => {
                    console.log(err);
                    _show_log("Error authorizing the payment");
                });
            _show_log("on payment authorized waiting");
        };
        session.oncancel = event => {
            _show_log("on cancel complete");
        };
        session.begin();


    });
};
function _show_log(msg, error) {
    if (error) {
        console.error(msg, error);
    } else {
        console.log(msg);
    };
    // document.getElementById('pnl_log').innerText = "\n" + msg;
};
function getCardType(cardNumber) {
    var cardPatterns = {
        visa: /^4[0-9]{12}(?:[0-9]{3})?$/,
        mastercard: /^5[1-5][0-9]{14}$/,
        amex: /^3[47][0-9]{13}$/,
        discover: /^6(?:011|5[0-9]{2})[0-9]{12}$/,
        mada: /^(588845|968208|636120|968201|455708|968205|588848|968203|504300|968211|968206|968202|968204|968207)\d{10}$/,
    };

    for (var cardType in cardPatterns) {
        if (cardPatterns[cardType].test(cardNumber)) {
            return cardType;
        }
    }
    return null;
}



const acceptCyberSourceMixin = {

    _prepareInlineForm(providerId, providerCode, paymentOptionId, paymentMethodCode, flow) {
        if (!(providerCode !== 'clickpay' || providerCode !== 'clickpaycard' || providerCode !== 'clickpayamex' || providerCode !== 'clickpaymada' || providerCode !== 'clickpayapplepay' || providerCode !== 'clickpayapplepayhosted')) {
            this._super(...arguments);
            return;
        };
        console.log(this);
        const provider = providerCode;
        console.log('flow :: ',flow);
        console.log('provider::', provider);
        if (providerCode=='clickpayapplepay'){document.getElementById('applepaybutton').style.display = 'none';return;};
        console.log('code 1881');
        if (provider === 'clickpay' || provider === 'clickpaycard' || provider === 'clickpaymada' || provider === 'clickpayamex') {
            const radio = document.querySelector('input[name="o_payment_radio"]:checked');
            const formType = this._getPaymentOptionType(radio);
            const $Formiframe = this.$(`#o_payment_${formType}_inline_form_${paymentOptionId} form`);
            const $Formmanaged = this.$(`#o_payment_${formType}_inline_form_${paymentOptionId} iframe`);
            if ($Formiframe.length > 0 || $Formmanaged.length > 0) {
                const $inlineForm = this.$(`#o_payment_${formType}_inline_form_${paymentOptionId}`);
                if ($inlineForm.length > 0) {
                    $inlineForm.removeClass('d-none');
                }
            }

        }
        else if (provider === 'clickpayapplepay' || provider === 'clickpayapplepayhosted') {
            console.log('code 1771');
            return;
        }
        else {
            console.log('code 1991');
            const radio = document.querySelector('input[name="o_payment_radio"]:checked');
            const formType = $(radio).data('payment-option-type');
            const $inlineForm = this.$(`#o_payment_${formType}_inline_form_${paymentOptionId}`);
            if ($inlineForm.children().length > 0) {
                $inlineForm.removeClass('d-none');
            };
        }
    },
    _processRedirectFlow(providerCode, paymentOptionId, paymentMethodCode, processingValues) {
        var code = providerCode;
            if (code === 'clickpay' || code === 'clickpaycard' || code === 'clickpaymada' || code === 'clickpayamex' || code === 'clickpayapplepay' || code === 'clickpayapplepayhosted') {
                cart_data = {
                    'code': code,
                    'reference': processingValues.reference,
                    'values': {
                        'amount': processingValues.amount,
                        'currency': processingValues.currency_id,
                        'partner': processingValues.partner_id,
                        'order': processingValues.reference
                    }
                };
                return this.rpc('/payment/clickpay/iframe_payment',
                    {
                        'code': code,
                        'reference': processingValues.reference,
                        'values': {
                            'amount': processingValues.amount,
                            'currency': processingValues.currency_id,
                            'partner': processingValues.partner_id,
                            'order': processingValues.reference
                        }
                    }
                ).then(response => {
                    $('.o_blockUI').remove();
                    if(code === 'clickpayapplepayhosted'){
                        const $paybutton = $('span[class="o_loader"]');
                        $paybutton.attr('class', 'd-none');
                        console.log(response.redirect_url);
                        window.location.href = response.redirect_url;
                        return;
                    }
                    if (response.status) {
                        if (code === 'clickpayapplepay') {
                            apple_pay_request = response.data.data;
                            document.getElementById('applepaybutton').style.display = 'block';
                        }
                        else if (response.type == "iframe") {
                            if (response.data.redirect_url) { 
                                var src = response.data.redirect_url
                                var selected_option = document.getElementById(`o_payment_method_${paymentOptionId}`).parentElement.parentElement.parentElement.parentElement;
                                var payment_iframe_div = selected_option.querySelector('#payment_iframe_div');
                                payment_iframe_div.insertAdjacentHTML('beforebegin',`<iframe src="${src}" width="100%" height="auto" style="min-width: auto; min-height: 400px; border: 0">`); 
                            } else {
                                // Handle the case where redirect URL is not available or the request was not successful
                                this._displayErrorDialog(
                                    _t("Server Error"),
                                    _t("Error processing payment request.")
                                );
                                console.error('Error processing payment request.');
                            }
                        }
                        else if (response.type == "managed_form") {
                            const id = response.data
                            var htmlCode = `<form action="/payment/clickpay/request" id="payform" method="post" style="width:40%">
                                    <span id="paymentErrors" style="color: #ff0033;"></span>
                                    <div class="row">
                                        <label style="font-size:12px;font-weight: normal !important; line-height: 1.3em;
                                            color: #a2a2a2;padding-bottom:0.2rem;padding-left:0;">Name</label>
                                        <div class="name-field" style="padding:0;">
                                            <input type="text" data-paylib="name" size="20" style="width:100%;padding:0.7%;padding-left:0.4rem;" value="Mitchell Admin">
                                        </div>
                                    </div>
                                    <div class="row">
                                        <label style="font-size:12px;font-weight: normal !important;line-height: 1.3em;
                                        color:#a2a2a2;padding-bottom:0.2rem;padding-left:0;">Card Number</label>
                                        <div class="name-field" style="padding:0;">
                                            <input type="text" data-paylib="number" size="20" id="cardnumber" style="width:100%;padding:0.7%;padding-left:0.4rem;margin:0;">
                                            <img src="/payment_clickpay/static/description/mada.png" class="ccicon" style="">
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="label" style="align-itmes:center; display:flex;gap:34px;padding:0;">
                                            <label style="width:47%;font-size: 12px;font-weight: normal !important;line-height: 1.3em;color: #a2a2a2;padding-bottom:0.2rem;padding-left:0;">Expiry Date (MM/YYYY)</label>   <label style="width:28%; font-size: 12px;font-weight: normal !important;line-height: 1.3em;
                                            color: #a2a2a2;padding-bottom:0.2rem;padding-left:0;">CVV</label>
                                        </div>
                                       <div class="expiry-date flex align-itmes-center"style="width:100%;gap: 7px;display: flex;padding:0;">
                                            <input type="text" data-paylib="expmonth" size="2" style="width: 24%;padding:0.7%;padding-left:0.4rem;">
                                            <span style="font-size:20px;display: flex;align-items: center;">/</span>
                                            <input type="text" data-paylib="expyear" size="4" style="width:24%;padding:0.7%;padding-left:0.4rem;">
                                            <input type="text" data-paylib="cvv" size="4" style="width: 52%;padding:0.7%;margin-left:1%;padding-left:0.4rem;">
                                        </div>
                                    </div>
                                    <div class="row my-4" >
                                        <div class="submit-button" style="padding:0;">
                                            <input type="submit" id="manage-form-submit-button" value="Place order" class="btn-primary"
                                            style="font-weight: 600; font-weight: 400;line-height: 1.5;border:0;text-align: center;vertical-align: middle;user-select: none;padding: 0.5rem 0.75rem;font-size: 1rem;border-radius: 0.25rem;color:black;background-color:lemon;">
                                        </div>
                                    </div>
                                    <input type="hidden" name="reference" value="${processingValues.reference}">
                                    <input type="hidden" name="partner" value="${processingValues.partner_id}">
                                    <input type="hidden" name="currency" value="${processingValues.currency_id}">
                                    <input type="hidden" name="amount" value="${processingValues.amount}">
                                    <input type="hidden" name="code" value="${code}">
                                    <input type="hidden" id="code-input" value="${code}">
                                    
                                </form>

                            `;
                            var selected_option = document.getElementById(`o_payment_method_${paymentOptionId}`).parentElement.parentElement.parentElement.parentElement;
                            var payment_iframe_div = selected_option.querySelector('#payment_iframe_div');
                            const parser = new DOMParser();
                            const formElement = parser.parseFromString(htmlCode, 'text/html').body.firstChild;
                            payment_iframe_div.appendChild(formElement);

                            const head = document.getElementsByTagName('head')[0];
                            const script = document.createElement('script');
                            script.src = 'https://secure.clickpay.com.sa/payment/js/paylib.js';
                            head.appendChild(script);
                            console.log('scriptinjected');

                            var myform = document.getElementById('payform');
                            console.log(myform);
                            paylib.inlineForm({
                                'key': id,
                                'form': myform,
                                'autosubmit': true,
                                'callback': function(response) {
                                    document.getElementById('paymentErrors').innerHTML = '';
                                    if (response.error) {
                                        paylib.handleError(document.getElementById('paymentErrors'), response);
                                    }
                                }
                            });

                            document.getElementById('payform').insertAdjacentHTML('afterend',`
                        <style>
                            .name-field{
                                position:relative;
                            }
                            .name-field img {
                                position: absolute;
                                right: 0;
                                top:0;
                                height: 60%;
                                transform: translate(-30%,30%) !important;
                            }
                            .row{
                                padding-left:10%;
                            }
                            @media all and (max-width:851px){
                                .row{
                                    width:100%;
                                    padding-left:10%;
                                }
                                form#payform {
                                    width: 100% !important;
                                }
                                }	
                                @media all and (max-width:767px){
                                    .row{
                                        width:100%;
                                        padding-left:10%;
                                    }
                                    form#payform {
                                        width: 100% !important;
                                    }
                                    }	
                        </style>`);
                            payment_iframe_div.style.display = 'block';
                            console.log(payment_iframe_div);
                            console.log('updated code 100');
                        }
                        else {
                            if (response.data.redirect_url) {
                                window.location = response.data.redirect_url
                            } else {
                                this._displayErrorDialog(
                                    _t("Server Error"),
                                    _t("Error processing payment request.")
                                );
                                console.error('Error processing payment request.');
                            }
                        }
                    } else {
                        this._displayErrorDialog(
                            _t("Server Error"),
                            _t("Error processing payment request.")
                        );
                    }
                });
                //    }).then(() => $('#payment_iframe').attr('src', api_url) );
            }
            else {
                return this._super(...arguments);
            }

    }
    // _initiatePaymentFlow: function (providerCode, paymentOptionId, paymentMethodCode, flow) {
    //     
    // },
};

checkoutForm.include(acceptCyberSourceMixin);
manageForm.include(acceptCyberSourceMixin);
