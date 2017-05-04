# encoding=utf8

import time
import paypal_utils


def main():
    while True:
        ipn_data = paypal_utils.get_not_verified_ipn_data()
        if not ipn_data:
            time.sleep(5)
            print 'no data'
            continue
        res = paypal_utils.verify_ipn_data(ipn_data)
        print 'check data:', ipn_data
        print 'result:', res


if __name__ == '__main__':
    main()
