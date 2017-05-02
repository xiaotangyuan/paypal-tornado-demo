# encoding=utf8

import os
import sys
import tornado.ioloop
import tornado.web
import handlers


url_conf = [
    (r"/", handlers.MainHandler),
]

application = tornado.web.Application(
    handlers=url_conf,
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
)

if __name__ == "__main__":
    PORT = sys.argv[1]
    application.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()
