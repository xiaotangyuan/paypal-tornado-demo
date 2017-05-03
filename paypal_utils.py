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
    params = parse_qs(urlparse(ipn_query_data).query)
    params = dict([(key, value[0]) for key, value in params.items()])
    params['cmd'] = '_notify-validate'
    # print params
    # params = {}
    headers = {'content-type': 'application/x-www-form-urlencoded', 'host': 'www.paypal.com'}
    # print params
    r = requests.post(VERIFY_URL, data=params, verify=True)
    r.raise_for_status()
    # print r.text[:100]
    if r.text == 'VERIFIED':
        return True
    else:
        return False


if __name__ == '__main__':
    data = 'payment_type=echeck&payment_date=Wed%20May%2003%202017%2017%3A20%3A58%20GMT%2B0800%20%28%u4E2D%u56FD%u6807%u51C6%u65F6%u95F4%29&payment_status=Completed&address_status=confirmed&payer_status=verified&first_name=John&last_name=Smith&payer_email=buyer@paypalsandbox.com&payer_id=TESTBUYERID01&address_name=John%20Smith&address_country=United%20States&address_country_code=US&address_zip=95131&address_state=CA&address_city=San%20Jose&address_street=123%20any%20street&business=seller@paypalsandbox.com&receiver_email=seller@paypalsandbox.com&receiver_id=seller@paypalsandbox.com&residence_country=US&item_name=something&item_number=AK-1234&quantity=1&shipping=3.04&tax=2.02&mc_currency=USD&mc_fee=0.44&mc_gross=12.34&mc_gross_1=12.34&txn_type=web_accept&txn_id=297635871&notify_version=2.1&custom=xyz123&invoice=abc1234&test_ipn=1&verify_sign=AQU0e5vuZCvSg-XJploSa.sGUDlpAEGPKt8ZHfdUfGxL2p9UvE4Ivsk8'
    verify_ipn_data(data)
