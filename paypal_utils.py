# encoding=utf8

import uuid
import paypal_settings


def get_paypal_button_info():
    button_info = {}
    if paypal_settings.USE_SANDBOX is True:
        button_info['business'] = paypal_settings.BUSINESS_EMAIL_SANDBOX
        button_info['notify_url'] = paypal_settings.NOTIFY_URL_SANDBOX
    else:
        button_info['business'] = paypal_settings.BUSINESS_EMAIL_LIVE
        button_info['notify_url'] = paypal_settings.NOTIFY_URL_LIVE
    # 订单号
    button_info['invoice'] = uuid.uuid1()
    # 订单金额
    button_info['amount'] = 199.00
    return button_info


def get_ipn_url():
    if paypal_settings.USE_SANDBOX is True:
        url = paypal_settings.VERIFY_URL_SANDBOX
    else:
        url = paypal_settings.VERIFY_URL_LIVE
    return url
