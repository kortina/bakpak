#!/usr/bin/env python
#
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
import logging

define("port", default=8888, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    def write_head(self):
        self.write('<script type="text/javascript" src="/cached.js"></script>')

    def print_and_set_headers(self, headers, do_print=True):
        for k, v in headers.iteritems():
            if do_print:
                self.write("<br />")
                self.write("%s: %s" % (k,v))
            self.set_header(k, v)

class MainHandler(BaseHandler):
    def get(self):
        self.write("Hello, world")

class CachePrivateHandler(BaseHandler):
    def get(self):
        logging.info(self)
        self.write_head()
        headers = {"Cache-Control": "public, max-age=31104000"}
        self.print_and_set_headers(headers)

class CacheJsHandler(BaseHandler):
    def get(self):
        logging.info(self)
        headers = {"Cache-Control": "public, max-age=31104000"}
        self.print_and_set_headers(headers, do_print=False)
        self.write('window.cachedjs=1;')


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/pr", CachePrivateHandler),
        (r"/cached.js", CacheJsHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
