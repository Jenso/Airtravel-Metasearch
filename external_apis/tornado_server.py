import tornado.ioloop
import tornado.web
from tornado import httpclient
import mongoengine
import json
import elementtree.ElementTree as ET

# init mongodb connection
MONGO_DATABASE_NAME = 'trip'
db = mongoengine.connect(MONGO_DATABASE_NAME)

def create_url(url, get_parameters):
    url += "?"
    for key in get_parameters:
        url += key + "=" + get_parameters[key] + "&"
    print url
    return url[:-1]

def parse_xml(data):
    xml_parsed = ET.parse("test.xml")
    i = 0
    for child in xml_parsed.getroot():
    #xml_parsed = ET.XML(data)
    #import pdb;pdb.set_trace()
    #for child in xml_parsed:
        dictionary = {}
        dictionary['total_price'] = int(child.find("total-price").text)
        dictionary['currency'] = child.find("currency").text
        dictionary['deeplink'] = child.find("deeplink").text

        # outbound
        dictionary['outbound'] = {}
        outbound = dictionary['outbound']
        outbound['departure-when'] = child.find("outbound/departure-when").text
        outbound['arrival-when'] = child.find("outbound/arrival-when").text
        outbound['departure-where-name'] = child.find("outbound/departure-where-name").text
        outbound['arrival-where-name'] = child.find("outbound/arrival-where-name").text
        outbound['arrival-where-code'] = child.find("outbound/arrival-where-code").text
        outbound['stops'] = child.find("outbound/stops").text
        outbound['airlines'] = child.find("outbound/airlines").text
        outbound['flightnumbers'] = child.find("outbound/flightnumbers").text

        trips_ele = child.find("outbound/trips")
        outbound['trips'] = []
        trips = outbound['trips']
    
        for trip in trips_ele:
            trip_dict = {}
            trip_dict['departure-when'] = trip.find("departure-when").text
            trip_dict['departure-where-name'] = trip.find("departure-where-name").text
            trip_dict['departure-where-code'] = trip.find("departure-where-code").text
            trip_dict['airline'] = trip.find("airline").text
            trip_dict['flightnumber'] = trip.find("flightnumber").text
            trip_dict['arrival-when'] = trip.find("arrival-when").text
            trip_dict['arrival-where-name'] = trip.find("arrival-where-name").text
            trip_dict['arrival-where-code'] = trip.find("arrival-where-code").text
        
            trips.append(trip_dict)


        # inbound
        dictionary['inbound'] = {}
        inbound = dictionary['inbound']
        inbound['departure-when'] = child.find("inbound/departure-when").text
        inbound['arrival-when'] = child.find("inbound/arrival-when").text
        inbound['departure-where-name'] = child.find("inbound/departure-where-name").text
        inbound['arrival-where-name'] = child.find("inbound/arrival-where-name").text
        inbound['arrival-where-code'] = child.find("inbound/arrival-where-code").text
        inbound['stops'] = child.find("inbound/stops").text
        inbound['airlines'] = child.find("inbound/airlines").text
        inbound['flightnumbers'] = child.find("inbound/flightnumbers").text
    
        trips_ele = child.find("inbound/trips")
        inbound['trips'] = []
        trips = inbound['trips']
    
        for trip in trips_ele:
            trip_dict = {}
            trip_dict['departure-when'] = trip.find("departure-when").text
            trip_dict['departure-where-name'] = trip.find("departure-where-name").text
            trip_dict['departure-where-code'] = trip.find("departure-where-code").text
            trip_dict['airline'] = trip.find("airline").text
            trip_dict['flightnumber'] = trip.find("flightnumber").text
            trip_dict['arrival-when'] = trip.find("arrival-when").text
            trip_dict['arrival-where-name'] = trip.find("arrival-where-name").text
            trip_dict['arrival-where-code'] = trip.find("arrival-where-code").text
        
            trips.append(trip_dict)
    

        toHex = lambda x:"".join([hex(ord(c))[2:].zfill(2) for c in x])
        #        dictionary['_id'] = toHex("".join([child.find("outbound/departure-when").text, child.find("outbound/flightnumbers").text]))
        #import pdb;pdb.set_trace()
        db.trip.trips.insert(dictionary)
        i += 1
    print i

class MainHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "".join(['POST','GET','OPTIONS', 'PUT', 'DELETE']))
    
    @tornado.web.asynchronous
    def get(self):
        print self.request.arguments
        http = httpclient.AsyncHTTPClient()
        """
        http.fetch(create_url("http://www.ticket.se/internal/cache/search/air",{"tripType":"ROUNDTRIP", "departureIata":"CPH", "arrivalIata":"NCE", "departureDate":"2012-11-01", "returnDate":"2012-11-06", "ticketType":"ECONOMY", "adults":"1", "children":"0", "infants":"0", "source":"zanox"}),
                   callback=self.on_response)
        """
        self.on_response("asd")
    def on_response(self, response):
        # TODO: Should LOG this
        #if response.error:
        #    raise tornado.web.HTTPError(500)

        #parse_xml(response.body)
        parse_xml(response)
        self.on_parsing_done()

    def on_parsing_done(self):
        data = db.trip.trips.find().sort('total_price',1)
        data = list(data)
        for d in data:
            if '_id' in d:
                d['_id'] = str(d['_id'])
                
        self.write(json.dumps(data))
        self.finish()
        #db.trip.trips.remove()


application = tornado.web.Application([
    (r"/", MainHandler),
], debug=True)

if __name__ == "__main__":
    print "Reload"
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
