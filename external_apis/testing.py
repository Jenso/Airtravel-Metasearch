import drest
#from elementtree import ElementTree
import elementtree.ElementTree as ET

"""
api = drest.API('http://www.ticket.se/internal/cache/search', trailing_slash=False, deserialize=False)
api.add_resource('air')
c = api.air.get(params={"tripType":"ROUNDTRIP", "departureIata":"CPH", "arrivalIata":"NCE", "departureDate":"2012-11-01", "returnDate":"2012-11-06", "ticketType":"ECONOMY", "adults":"1", "children":"0", "infants":"0", "source":"zanox"})
"""

# should probably do this with a stream, straight from the network card
#xml_parsed = ET.XML(c.data)
xml_parsed = ET.parse("test.xml")


from pymongo import Connection
connection = Connection()
db = connection.trip
collection = db.test_collection
i = 0
print xml_parsed
collection.remove()

def time_difference(x, y):
    from datetime import datetime
    x = datetime.strptime(x, "%Y-%m-%dT%H:%M")
    y = datetime.strptime(y, "%Y-%m-%dT%H:%M")
    return y-x

for child in xml_parsed.getroot():
    dictionary = {}
    dictionary['total-price'] = int(child.find("total-price").text)
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
    
    i += 1
    #print
    toHex = lambda x:"".join([hex(ord(c))[2:].zfill(2) for c in x])
    dictionary['_id'] = toHex("".join([child.find("outbound/departure-when").text, child.find("outbound/flightnumbers").text]))
    collection.insert(dictionary)
    #print dictionary
    #import pdb;pdb.set_trace()

print i
