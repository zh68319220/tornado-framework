# encoding=utf-8
import tornado.web
import logging as l

class BaseHandler(tornado.web.RequestHandler):
    def db(self):
        return 0