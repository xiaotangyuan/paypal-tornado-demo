# encoding=utf8

import urllib
import tornado
import tornado.gen
import tornado.web
import tornado.httpclient
import paypal_utils 


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        button_info = paypal_utils.get_paypal_button_info()
        self.render('index.html', button_info=button_info)


class IPNHandler(tornado.web.RequestHandler):
    """
    接受来自paypal的IPN通知
    1. PayPal 以 HTTP POST 方式向此侦听器传递一条 IPN 消息，通知发生了一个事件。
    2. 侦听器向 PayPal 返回一条空白的 HTTP 200 消息。
    3. 侦听器以 HTTP POST 方式将完整的、未更改的消息发回 PayPal；此消息中必须包含与原
    消息相同的字段（按照相同顺序），并采用与原消息相同的编码方式。
    4. PayPal 发回一条只有一个词的消息—— VERIFIED （如果消息与原消息一致）或 INVALID （如
    果消息与原消息不一致）。

    步骤3,4需要单独的服务（进程）完成
    此handler完成步骤1,2，将 来自paypal的IPN通知数据保存已被步骤3,4 使用

    防止第一步的IPN伪造通知：
    # 生成一个密钥（需要保存） 用自定义变量形式在支付时一起提交到paypal，然后在ipn通知时 判断paypal的通知消息里含有 正确的密钥
    """
    @tornado.gen.coroutine
    def post(self, live_or_sandbox):
        print 'live_or_sandbox:', live_or_sandbox
        ipn_data = self.request.body
        # 此处需要先检查ipn_data中是否包含正确的custom (密钥) needfix
        paypal_utils.save_ipn_data(ipn_data)
        self.finish()
        return
