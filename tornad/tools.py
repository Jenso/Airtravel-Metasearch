import elementtree.ElementTree as ET
from tornad.database import *
import tornado, re

def create_url(url, get_parameters):
    url += "?"
    for key in get_parameters:
        url += key + "=" + get_parameters[key] + "&"
    print url
    return url[:-1]

def parse_xml(data, travel_agency):
    if USE_LOCAL_XML:
        xml_parsed = ET.parse("tornad/data/example_trip_data.xml").getroot()
    else:
        xml_parsed = ET.XML(data)

    for child in xml_parsed:
        dictionary = {}
        # Should be conditional
        dictionary['total_price'] = int(child.find("total-price").text)
        dictionary['currency'] = child.find("currency").text
        dictionary['deeplink'] = child.find("deeplink").text

        dictionary['prices'] = [{'travel_agency': travel_agency,
                                 'price': dictionary['total_price']}]
        
        # outbound
        dictionary['outbound'] = {}
        outbound = dictionary['outbound']
        outbound['departure-when'] = child.find("outbound/departure-when").text
        outbound['departure-where-name'] = child.find("outbound/departure-where-name").text
        outbound['departure-where-code'] = child.find("outbound/departure-where-code").text
        outbound['arrival-when'] = child.find("outbound/arrival-when").text
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
        inbound['departure-where-name'] = child.find("inbound/departure-where-name").text
        inbound['departure-where-code'] = child.find("inbound/departure-where-code").text
        inbound['arrival-when'] = child.find("inbound/arrival-when").text
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

def validate_get_params(parameters):
    #import pdb;pdb.set_trace()
    # Should log all these too
    validated_parameters = {}
    expected_parameters = ['tripType', 'departureIata', 'arrivalIata', 'departureDate',
                           'returnDate', 'ticketType', 'adults', 'children', 'infants']

    for parameter in expected_parameters:
        if not parameters(parameter):
            raise tornado.web.HTTPError(400, "Parameter not found: " + parameter)

    print parameters
    if not parameters('tripType') in ['ROUNDTRIP', 'ONEWAY']:
        raise tornado.web.HTTPError(400, "Bad parameters")
    validated_parameters['tripType'] = parameters('tripType')
    
    if not parameters('ticketType') in ['ECONOMY', 'BUSSINESS']:
        raise tornado.web.HTTPError(400, "Bad parameters")
    validated_parameters['ticketType'] = parameters('ticketType')

    for iata_name in ['arrivalIata', 'departureIata']:
        iata_val = parameters(iata_name)
        if not len(iata_val) == 3 or not len(re.findall("[A-Z]", iata_val)) == 3:
            raise tornado.web.HTTPError(400, "Bad parameters")
        validated_parameters[iata_name] = iata_val

    for date_param in ['departureDate', 'returnDate']:
        if not re.match("201[2-9]-[01]\d-[0123]\d", parameters(date_param)):
            raise tornado.web.HTTPError(400, "Bad parameters")
        validated_parameters[date_param] = parameters(date_param)

    for param_name in ['adults', 'children', 'infants']:
        try:
            param_int = int(parameters(param_name))
        except ValueError:
            raise tornado.web.HTTPError(400, "Bad parameters")

        if param_int < 0 or param_int > 10:
            raise tornado.web.HTTPError(400, "Bad parameters")
        
        validated_parameters[param_name] = parameters(param_name)

    return validated_parameters
         
