import tornado
from tornad.handlers import TripsHandler, AirportsHandler
from tornad.database import *

routes = [(r"/", TripsHandler),
          (r"/airports/", AirportsHandler),
          ]

def start_tornado():
    """
    Start in dev
    """
    application = tornado.web.Application(routes, debug=True)
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

    
def start_tornado_production():
    """
    Start as daemon
    """
    import daemon
    log = open('/var/log/tornado/tornado.log', 'a+')
    # TODO: Doesnt create .pidfile for some reason
    ctx = daemon.DaemonContext(stdout=log, stderr=log,  working_directory='.', pidfile="/tmp/tornado.pid")
    if ctx.is_open:
        ctx.close()
        
    ctx.open()
    application = tornado.web.Application(routes, debug=True)

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    start_tornado_production()
else:
    start_tornado()
