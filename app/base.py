# encoding=utf-8
import tornado.web
import json
import logging as l

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie("u")

    def write(self, data):
        cb = self.get_argument("callback", None)
        if cb is not None:
            super(BaseHandler, self).write(cb + '(' + json.dumps(data) + ')')
            self.set_header('Content-Type', 'application/javascript')
        else:
            super(BaseHandler, self).write(json.dumps(data))
            self.set_header('Content-Type', 'application/json')