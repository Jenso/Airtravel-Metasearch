import elementtree.ElementTree as ET
from tornad.database import *

def create_url(url, get_parameters):
    url += "?"
    for key in get_parameters:
        url += key + "=" + get_parameters[key] + "&"
    print url
    return url[:-1]

def parse_xml(data):
    if USE_LOCAL_XML:
        xml_parsed = ET.parse("tornad/data/example_trip_data.xml").getroot()
    else:
        xml_parsed = ET.XML(data)

    for child in xml_parsed:
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
