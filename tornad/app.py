import tornado
from tornad.handlers import TripsHandler, AirportsHandler

application = tornado.web.Application([
    (r"/", TripsHandler),
    (r"/airports/", AirportsHandler),
    ], debug=True)

application.listen(8888)
tornado.ioloop.IOLoop.instance().start()
