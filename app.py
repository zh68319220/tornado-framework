import tornado.ioloop,tornado.web,\
    tornado.httpserver,tornado.process,\
    tornado.netutil,tornado.locale, os
from tornado.options import options, define
import logging as l
from urls import urls
import app.torndb as db

class Application(tornado.web.Application):
    def __init__(self):
        settings = {
            'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
            'static_path': os.path.join(os.path.dirname(__file__), 'assets'),
            'static_url_prefix': '/assets/',
            'cookie_secret': 'f',
            'cookie_domain': 'localhost',
            'login_url': '/login',
            'debug': True,
            'xsrf_cookies': True,
        }
        super(Application, self).__init__(urls, **settings)

        self.db = torndb.Connection("localhost", "blog")

if __name__ == "__main__":
    # tornado.locale.load_translations(os.path.join(options.run_path, "locale"))
    tornado.options.parse_config_file('app/config.conf')
    tornado.options.parse_command_line()
    app = Application()
    if True:
        print('debug --------------------')
        server = tornado.httpserver.HTTPServer(app, xheaders=True)
        server.listen(3000)
    else:
        print('run --------------------')
        sockets = tornado.netutil.bind_sockets(options.port)
        tornado.process.fork_processes(0)
        server = tornado.httpserver.HTTPServer(app, xheaders=True)
        server.add_sockets(sockets)
    tornado.ioloop.IOLoop.current().start()