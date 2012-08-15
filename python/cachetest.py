#!/usr/bin/env python
import datetime
import logging
#
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import re

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    def write_head(self):
        version = '1'
        m = re.search(r"/[a-zA-Z_]+(\d+)", self.request.path)
        if m and m.group(1):
            version = m.group(1)
        self.write('<script type="text/javascript" src="/cached%s.js"></script>' % version)

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
        headers = {"Cache-Control": "private, max-age=60"}
        self.print_and_set_headers(headers)

class CacheJsHandler(BaseHandler):
    def get(self):
        logging.info(self)
        headers = {"Cache-Control": "public, max-age=60"}
        self.print_and_set_headers(headers, do_print=False)
        self.write('window.cachedjs=1;')

class CacheManifestHandler(BaseHandler):
    def get(self):
        logging.info(self)
        html = """
<!DOCTYPE HTML>
<html manifest="c.appcache">
 <head>
  <title>Demo</title>
 </head>
 <body>
  <p>The time is: %s</p>
 </body>
</html>
""" % datetime.datetime.now()
        self.write(html)

class AppcacheHandler(BaseHandler):
    def get(self):
        logging.info(self)
        self.write("CACHE MANIFEST\n")
        self.write("cm\n")
        self.write("# 2010-06-18:v3\n")
        self.write("\n")
        self.write("# Explicitly cached entries\n")
        headers = {"Content-Type": "text/cache-manifest"}
        self.print_and_set_headers(headers, do_print=False)

def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/pr\d{0,4}", CachePrivateHandler),
        (r"/cm\d{0,4}", CacheManifestHandler),
        (r"/c.appcache", AppcacheHandler),
        (r"/cached\d{0,4}.js", CacheJsHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
