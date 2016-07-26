#encoding=utf-8
import app.base as base
import logging as l

class MainHandler(base.BaseHandler):
    '''
    yf: 首页
    '''
    def get(self):
        users = self.db.query("SELECT * FROM user ORDER BY username "
            "DESC LIMIT 10")
        self.write({'users': users})