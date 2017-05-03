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
    """
    @tornado.gen.coroutine
    def get(self):
        self.finish()
        return
