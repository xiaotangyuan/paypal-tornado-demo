# encoding=utf8

import uuid
from urlparse import parse_qs, urlparse
import requests
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
    # 防止IPN伪造通知：
    # 生成一个密钥 用自定义变量形式在支付时一起提交到paypal，然后在ipn通知时 判断paypal的通知消息里含有 正确的密钥
    # 此处需要保存这个密钥以便PayPal通知时检查custom  needfix
    button_info['custom'] = uuid.uuid1()
    return button_info


def get_ipn_url():
    if paypal_settings.USE_SANDBOX is True:
        url = paypal_settings.VERIFY_URL_SANDBOX
    else:
        url = paypal_settings.VERIFY_URL_LIVE
    return url


def verify_ipn_data(ipn_query_data):
    params = 'cmd=_notify-validate&' + ipn_query_data
    VERIFY_URL = get_ipn_url()
    # params = parse_qs(urlparse(ipn_query_data).query)
    # params = dict([(key, value[0]) for key, value in params.items()])
    # params['cmd'] = '_notify-validate'
    print params
    headers = {'content-type': 'application/x-www-form-urlencoded', 'host': 'www.paypal.com'}
    r = requests.post(VERIFY_URL, data=params, verify=True)
    r.raise_for_status()
    print r.text[:100]
    if r.text == 'VERIFIED':
        return True
    else:
        return False


def save_ipn_data(ipn_data):
    import redis
    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    r.rpush('ipn_data_queue', ipn_data)


def get_not_verified_ipn_data():
    import redis
    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    return r.lpop('ipn_data_queue')


if __name__ == '__main__':
    data = ''
    verify_ipn_data(data)
