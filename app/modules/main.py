# encoding: utf-8
from app.modules import base
import logging as l

class main(base):
    def render(self, template_name, **kwargs):
        super(main, self).render(template_name, **kwargs)

class MainHandler(main):
    '''
    yf: 首页
    '''
    def get(self):
        self.current_user = self.get_current_user()
        if self.current_user:
            self.render('object.new.html', hl='new-object')
        else:
            self.redirect('/login')

class ObjectAddHandler(main):
    '''
    yf: 编辑专题
    '''
    def get(self):
        pass

    def post(self):
        import os
        dat = self.json_decode(self.request.body)
        if 'id' not in dat: # 添加
            oid = self.db.object.add(**dat)
            if oid: # 添加模板
                ph = os.path.dirname(__file__).split("app")[0] + 'templates\\s\\'+str(oid)
                os.makedirs(ph)
                open("./templates/s/"+str(oid)+"/index.html", "w")
        else:
            pass

class ObjectsHandler(main):
    '''
    yf: 专题
    '''
    def get(self):
        objs = self.db.object().data
        self.render('object.list.html', hl='list-object', objs=objs)

class CateHandler(main):
    '''
    yf: 分类
    '''
    def get(self):
        cates = self.db.category().data
        self.render('cate.list.html', hl='list-cate', cates=cates)

class CateEditHandler(main):
    '''
    yf: 编辑分类
    '''
    def get(self):
        self.render('cate.edit.html', hl='edit-cate')

    def post(self):
        dat = self.json_decode(self.request.body)
        if 'id' in dat: # 编辑
            pass
        else: # 添加
            cid = self.db.category.add(**dat)
            if cid:
                self.redirect('/cate')

class LoginHandler(main):
    '''
    yf: 登录
    '''
    def get(self):
        if self.current_user:
            self.redirect('/')
        else:
            self.render('login.html')

    def post(self):
        dat = self.json_decode(self.request.body)
        u = self.db.user(username=dat['username'], password=dat['password']).one()
        if u:
            self.set_secure_cookie('u', unicode(u.id))
            self.redirect('/')
        else:
            self.render('login.html', error='用户名或密码错误')

class PagesHandler(main):
    def get(self, id=None):
        self.render('s\\'+id+'\\index.html')

class NotFoundHandler(main):
    def get(self):
        self.write("Sorry, Page not Found.. Go <a href=\"/\">back</a>")

url_prefix = ''

urls = [
    ('/', MainHandler),
    ('/objlist', ObjectsHandler),
    ('/objadd', ObjectAddHandler),
    ('/cate', CateHandler),
    ('/editcate', CateEditHandler),
    ('/login', LoginHandler),
    ('/s/(\d+)/', PagesHandler)
]