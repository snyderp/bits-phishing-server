import os
import config
import tornado.ioloop
import tornado.httpserver
import motor
import phishing.controllers as controllers
import phishing.debugging


settings = {
    "db": motor.MotorClient(**config.mongo_params)[config.mongo_database],
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug": config.debug,
}

routes = [
    (r"/register", controllers.Register),
    (r"/cookie-rules", controllers.CookieRules),
    (r"/password-entered", controllers.PasswordEntered),
    (r"/email", controllers.EmailUpdate),
    (r"/browsing-counts", controllers.BrowsingCounts),
    (r"/password-autofilled", controllers.PasswordAutofill)
]

if config.debug:
    routes.append((r"/cookie-set", controllers.CookieSetTest))

application = tornado.web.Application(routes, **settings)

if __name__ == "__main__":
    if config.ssl_options:
        server = tornado.httpserver.HTTPServer(
            application, ssl_options=config.ssl_options)
    else:
        server = tornado.httpserver.HTTPServer(application)

    if config.log_dir:
        phishing.debugging.configure_logger()

    server.listen(config.port)
    tornado.ioloop.IOLoop.instance().start()
