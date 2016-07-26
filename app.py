import tornado.ioloop,tornado.web,\
    tornado.httpserver,tornado.process,\
    tornado.netutil,tornado.locale, os
from tornado.options import options, define
import logging as l
from urls import urls
import torndb as db

define('mysql_database', default="test")
define('mysql_host', default="localhost")
define('mysql_user', default="0")
define('mysql_password', default="0")

define('debug', default=True)
define('template_path', default="templates")
define('static_path', default="assets")
define('static_url_prefix', default="/assets/")
define('cookie_secret', default="s")
define('cookie_domain', default="localhost")
define('login_url', default="/login")
define('xsrf_cookies', default=True)
define('port', default=8080)

class Application(tornado.web.Application):
    def __init__(self):
        settings = {
            'template_path': os.path.join(os.path.dirname(__file__), options.template_path),
            'static_path': os.path.join(os.path.dirname(__file__), options.static_path),
            'static_url_prefix': options.static_url_prefix,
            'cookie_secret': options.cookie_secret,
            'cookie_domain': options.cookie_domain,
            'login_url': options.login_url,
            'debug': options.debug,
            'xsrf_cookies': options.xsrf_cookies,
        }
        super(Application, self).__init__(urls, **settings)

        self.db = db.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)

if __name__ == "__main__":
    # tornado.locale.load_translations(os.path.join(options.run_path, "locale"))
    tornado.options.parse_config_file('app/config.conf')
    tornado.options.parse_command_line()
    app = Application()
    if options.debug:
        print('debug --------------------')
        server = tornado.httpserver.HTTPServer(app, xheaders=True)
        server.listen(options.port)
    else:
        print('run --------------------')
        sockets = tornado.netutil.bind_sockets(options.port)
        tornado.process.fork_processes(0)
        server = tornado.httpserver.HTTPServer(app, xheaders=True)
        server.add_sockets(sockets)
    tornado.ioloop.IOLoop.current().start()