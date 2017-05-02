# encoding=utf8

import sys
import tornado.ioloop
import tornado.web
import handlers


application = tornado.web.Application([
    (r"/", handlers.MainHandler),
])

if __name__ == "__main__":
    PORT = sys.argv[1]
    application.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()
