$.ajaxSetup({
    cache: false
});

Travel = new Backbone.Marionette.Application();

Travel.addRegions({
    mainRegion: "#content"
});

var Trip = Backbone.Model.extend({
    idAttribute: 'id', // resource_uri, sätts inte av vårt MongoDB/Tastypie api
    parseTime: function(date) {
        return date.split("T")[1];
    },
    parse: function(response) {
        // after a save on the model, parse is called with response==null
        if(response == null) return
        response.outbound_departure_time = this.parseTime(response.outbound['departure-when']);
        response.outbound_arrival_time = this.parseTime(response.outbound['arrival-when']);
        response.inbound_departure_time = this.parseTime(response.inbound['departure-when']);
        response.inbound_arrival_time = this.parseTime(response.inbound['arrival-when']);

        return response;
    }
});

var TripsCollection = Backbone.Collection.extend({
    url: TORNADO_API_URL,
    model: Trip
});

var AirportsCollection = Backbone.Tastypie.Collection.extend({
    url: AIRPORTS_API_URL
});

var AirportView = Backbone.Marionette.ItemView.extend({
});

var AirportSearchView = Backbone.Marionette.CompositeView.extend({
    itemView: AirportView
});

var OverlayView = Backbone.View.extend({
    el: $('body'),
    template: _.template($("#tpl-overlay").html()),
    className: "trip-overlay",
    tagName: "div",
    initialize: function(){
        dayOfOutboundDeparture = this.dayOfTravel('outbound', 'departure');
        dayOfOutboundArrival = this.dayOfTravel('outbound', 'arrival');
        dayOfInboundDeparture = this.dayOfTravel('inbound', 'departure');
        dayOfInboundArrival = this.dayOfTravel('inbound', 'arrival');

        this.model.set({
            'dayOfOutboundDeparture' : dayOfOutboundDeparture,
            'dayOfOutboundArrival' : dayOfOutboundArrival,
            'dayOfInboundDeparture' : dayOfInboundDeparture,
            'dayOfInboundArrival' : dayOfInboundArrival
        });
    },
    events: {
        'click #close-modal': 'closeTripOverlay'
    },
    weekday: [
        "Söndag",
        "Måndag",
        "Tisdag",
        "Onsdag",
        "Torsdag",
        "Fredag",
        "Lördag"
    ],

    dayOfTravel: function(when, what){
        var traveldate =  this.model.get(when)[what+'-when'].substr(0, 10);
        dt = new Date(traveldate).getDay();
        return this.weekday[dt];
    },
    render:function (eventName) {
        $(this.el).append(this.template(this.model.toJSON()));
        this.$('#overlay-modal').modal('show');
        return this;
    },
    destroy_view: function() {
        //COMPLETELY UNBIND THE VIEW
        this.undelegateEvents();

        $(this.el).removeData().unbind();

        //Remove view from DOM
        this.$('#overlay-modal').remove();
        Backbone.View.prototype.remove.call(this);
    },
    closeTripOverlay: function(){
        $('#overlay-modal').modal('hide');
    }
});

var TripView = Backbone.Marionette.ItemView.extend({
    template: "#tpl-trip",
    className: "trip",
    tagName: "li",
    onBeforeRender: function(){
        // sort agency prices array before render
        this.model.set('prices',this.model.get('prices').sort(function(a,b){
            return b.price - a.price;
        }));

    },

    airlinePicList: {
        'KLM Royal Dutch Airlines' : 'klm',
        'Scandinavian Airlines, SAS' : 'sas',
        'Brussels Airlines' : 'brusselsairlines',
        'Swiss' : 'swiss',
        'Lufthansa' : 'lufthansa',
        'Austrian Airlines' : 'austrianairlines',
        'Air France' : 'airfrance',
        'Iberia Airlines' : 'iberiaairlines',
        'Turkish Airlines' : 'turkishairlines',
        'United Airlines' : 'unitedairlines',
        'British Airways' : 'britishairways',
        'Air Canada' : 'aircanada',
        'Virgin Atlantic' : 'virginatlantic',
        'Emirates' : 'emirates',
        'Delta Air Lines' : 'deltaairlines',
        'US Airways' : 'usairways',
        'Gulf Air' : 'gulfair',
        'China Southern Airlines' : 'chinasouthernairlines',
        'Air China' : 'airchina',
        'Aeroflot' : 'aeroflot',
        'American Airlines' : 'americanairlines',
        'Finnair' : 'finnair',
        'Malaysia Airlines' : 'malaysiaairlines',
        'Qantas' : 'qantas',
        'Norwegian' : 'norwegian',
        'Singapore Airlines' :  'singaporeairlines',
        'TUIfly' : 'tuifly'
    },

    initialize: function(){

        this.model.set({
            'airlineOutbound' : this.currentAirplane('outbound')
        }, {silent:true});
        this.model.set({
            'airlineInbound' : this.currentAirplane('inbound')
        }, {silent:true});

    },
    events: {
        'click .flight-info-trigger': 'tripOverlay'
    },
    tripOverlay: function() {
        this.currentOverlay = new OverlayView({model: this.model, el: this.$('.modal-container')}).render();
    },
    currentAirplane: function(airplane){
        str = this.model.get(airplane).airlines;
        theAirlines = str.split(";");
        firstAirline = theAirlines[0];
        if(firstAirline in this.airlinePicList){
            return this.airlinePicList[firstAirline];
        }
        else{
            return "randomairplane";
        };
    }
});

var TripsView = Backbone.Marionette.CompositeView.extend({
    itemView: TripView,
    itemViewOptions: function() {
        return {
            departureTimezone: this.departureTimezone,
            arrivalTimezone: this.arrivalTimezone
        };
    },
    template: "#tpl-trips",
    tagName: "div",
    className: "search-result-list",
    initialize: function() {
        this.searchTerm = this.options.searchTerm;
        this.initTimezoneData();
        this.initCollection();
    },
    initCollection: function() {
        var _this = this;
        this.collection = new TripsCollection();
        this.collection.fetch({
            data: this.searchTerm,
            // since we trigger an event on success, that in turn trigger a render of this view.
            // we dont want to trigger a rendering of the view when the collection is fetched
            silent:true,
            success: function(collection, response) {
		if(collection.length > 0) {
                    Travel.vent.trigger("search:tripsloaded", _this)
		} else {
		    // no flights found for the search
		    Travel.vent.trigger("search:noflightsfound", _this)
		}
            }
        });
    },
    destroyView: function() {
        //COMPLETELY UNBIND THE VIEW
        this.undelegateEvents();

        $(this.el).removeData().unbind();

        Backbone.View.prototype.remove.call(this);
    },
 
    initTimezoneData: function() {
        // TODO: If TripsCollection query is done before this request, we have a problem -> FIX!
        var _this = this;
        $.ajax({
            url: AIRPORTS_API_URL,
            data: "iata__in=" + _this.searchTerm.departureIata + "&iata__in=" + _this.searchTerm.arrivalIata,
            success: function (response) {
                // timezone's are in GMT+XXXX (example: GMT+0100)
                var objects = response.objects;

                _this.departureTimezone = objects[0].timezone;
                _this.arrivalTimezone = objects[1].timezone;

            }
        });

    },
    appendHtml: function(collectionView, itemView, index){
        collectionView.$el.find("#search-results").append(itemView.el);
    }
});

var NoFlightsFoundView = Backbone.Marionette.ItemView.extend({
    template: "#tpl-no-flights-found"
});

var WaitingSearchView = Backbone.Marionette.ItemView.extend({
    template: "#tpl-waiting-search",

    onRender: function(){
        setInterval(this.loadTheBar,1);
    },


    loadTheBar: function(){
        widthNumber = this.$('#current-progress-bar').width();
        widthNumber = widthNumber + 30;
        this.$('#current-progress-bar').width(widthNumber);
    }

});

var SearchView = Backbone.Marionette.ItemView.extend({
    //itemView: PinView,
    template: "#tpl-search-area",
    initialize: function() {
        _.bindAll(this, 'onSelectDeparture', 'onSelectArrival');
    },
    onRender: function () {
        $.datepicker.regional['sv'] = {
            closeText: 'Stäng',
            prevText: '&laquo;Förra',
            nextText: 'Nästa&raquo;',
            currentText: 'Idag',
            monthNames: ['Januari','Februari','Mars','April','Maj','Juni',
                         'Juli','Augusti','September','Oktober','November','December'],
            monthNamesShort: ['Januari','Februari','Mars','April','Maj','Juni',
                              'Juli','Augusti','September','Oktober','November','December'],
            dayNamesShort: ['Sön','Mån','Tis','Ons','Tor','Fre','Lör'],
            dayNames: ['Söndag','Måndag','Tisdag','Onsdag','Torsdag','Fredag','Lördag'],
            dayNamesMin: ['Sö','Må','Ti','On','To','Fr','Lö'],
            weekHeader: 'v',
            dateFormat: 'yy-mm-dd',
            firstDay: 1,
            isRTL: false,
            showMonthAfterYear: false,
            minDate: 0,
            changeMonth:false,
            changeYear: false,
            showOtherMonths:true,
            selectOtherMonths:true,
            showWeek:true,
            yearSuffix: ''};
        $.datepicker.setDefaults($.datepicker.regional['sv']);
        var _this = this;
        this.$("#datepicker-departure-date").datepicker({firstDay: 1,
                                                         onSelect: this.onSelectDeparture});
        this.$("#datepicker-return-date").datepicker({firstDay: 1,
                                                      onSelect: this.onSelectArrival});
        this.initQuickselect();
        
    },
    onSelectDeparture: function(dateText, inst){
        this.departureDateFromDatepicker =  dateText;
        var chosenDate = new Date(dateText)
        this.$("#datepicker-return-date").datepicker('option', 'minDate', chosenDate);
    },
    onSelectArrival: function(dateText, inst) {
        this.arrivalDateFromDatepicker = dateText;
        
        departureDate = new Date(this.departureDateFromDatepicker);
        arrivalDate = new Date(this.arrivalDateFromDatepicker);
        this.dateValidation(departureDate, arrivalDate);
    },

    events: {
        'click #search-trip': 'searchTrip',
        'click #trip-type' : 'hideArrivalDate',
        'click #trip-type-tr' : 'hideArrivalDate'
    },
    initQuickselect: function() {
        // tell where QuickSelect should get the Airport data
        var options = {ajax: TORNADO_API_URL + "airports/", minChars: 2};
        this.$('input#from').quickselect(options);
        this.$('input#to').quickselect(options);
    },
    extractIata: function(str) {
        function trim(str) {
            return str.replace(/^\s\s*/, '').replace(/\s\s*$/, '');
        }
        return trim(str.split(",")[1]);
    },

    testNaN: function(parsedDate1, parsedDate2){
	    /* 	 Tests if the user has selected dates for his trip. Returns a number so the function which calls on testNaN can know what kind date is missing  */
	    
        if (parsedDate1 == undefined && parsedDate2 == undefined){
            alert("Error: Var god och välj datum för din resa.")
            return 2;
        }
        else if (parsedDate1 == undefined){
            alert("Error: Var god och välj datum för din utresa.")
            return 3;
        }
        else if (parsedDate2 == undefined){
            if(this.$('#trip-type').hasClass('active')){
                return 0;
            }
            else{
                alert("Error: Var god och välj datum för din hemresa.")
                return 4;
            }
        }
        else{
            null;
        }
    },

    dateValidation: function(date1, date2){
        if (date2 >= date1){
            return 0;
        }
        else if (date2 < date1){
            alert("Error: Ditt datum för utresa ligger efter ditt datum för hemresa, var god försök igen :) ");
            return 1;
        }
        else{
            return this.testNaN(date1, date2);
        }
    },
    
    inputValidation : function(inputtx, theWord){
        if (inputtx.val().length == 0){   
        	alert("Error: Du har visst glömt att fylla i vart du vill åka "+theWord+", var god försök igen :)")    
        	return false;   
        }       
        return true;   
    },
    
    validationTests : function(params){
	    /*  This function tests the users input */
	        
	    var testResponse = {
		/* 	This is to be able to return multiple values*/
		    'searchParams' : params,
		    'testOk' : false
		};
		    
		/*  Tests the users inputs     */
		var dateTest = this.dateValidation(testResponse.searchParams.departureDate, testResponse.searchParams.returnDate);
		var inputTestFrom = this.inputValidation(this.$('input#from'), "från");
		var inputTestTo = this.inputValidation(this.$('input#to'), "till");
	        
	        
		if (inputTestFrom && inputTestTo){
		/* 	If the input-forms contains a value it sets searchParams.departureIata to the inputs value */
			testResponse.searchParams.departureIata = this.extractIata(this.$('input#from').val());
			testResponse.searchParams.arrivalIata = this.extractIata(this.$('input#to').val());
		};
	        
	       
		if (dateTest == 0 && inputTestFrom && inputTestTo){
		/* If all the tests is OK, then it sets testResponse.testOk = True */
			testResponse.testOk = true;
		};
		    
		return testResponse;	    
    },

    searchTrip: function() {
        if(this.$('#trip-type').hasClass('active')) {
            var tripType = 'ONEWAY';
        } else {
            var tripType = 'ROUNDTRIP';
        }
        var searchParams = {
            'tripType': tripType,
            'departureIata': "",
            'arrivalIata': "",
            "departureDate": this.departureDateFromDatepicker,
            "returnDate": this.arrivalDateFromDatepicker,
            "ticketType":"ECONOMY",
            "adults": this.$('#number-adults').val(),
            "children": this.$('#number-children').val(),
            "infants":"0"
        };
        
        var testResponse = this.validationTests(searchParams);
        
        searchParams = testResponse.searchParams;
        
        if (testResponse.testOk == true){
	        Travel.vent.trigger("search:start", searchParams);
        };

    },

    hideArrivalDate: function(){
        if(this.$('#trip-type-tr').hasClass('active')){
        	this.$('#label-to-return-date').hide();
        	this.$('#datepicker-return-date').hide();
        }
        else if(this.$('#trip-type').hasClass('active')){
        	this.$('#label-to-return-date').show();
        	this.$('#datepicker-return-date').show();
        }
    }

});

Travel.addInitializer(function(options){
    function trackCategory(category) {
        _kmq.push(['record', 'Changed category', {'Category': category}]);
    }

    MyRouter = Backbone.Marionette.AppRouter.extend({
        routes : {
            "test-search" : "search",
            "*actions": "defaultRoute"
        },
        search: function() {
            var test_data =  {
                'tripType':'ROUNDTRIP',
                'departureIata': 'CPH',
                'arrivalIata': 'NCE',
                "departureDate":"2012-11-15",
                "returnDate":"2012-11-20",
                "ticketType":"ECONOMY",
                "adults":"1",
                "children":"0",
                "infants":"0"
            };

            Travel.vent.trigger("search:start", test_data);

        },
        defaultRoute: function() {



            //var collection = new PinsPagerCollection();
            var SearchView1 = new SearchView();

            Travel.mainRegion.show(SearchView1);

        }
    });

    Travel.vent.on("search:start", function(searchTerm){
        Travel.mainRegion.show(new WaitingSearchView());
        //Backbone.history.navigate("search/" + searchTerm);

        // An event will be triggered when TripsView have loaded everything
        // and set mainRegion.show on it
        var not_used = new TripsView({searchTerm: searchTerm});
    });


    Travel.vent.on("search:tripsloaded", function(tripsViewObj) {
        // searchQuery against travel agencies done, now show them
        Travel.mainRegion.show(tripsViewObj);
    });

    Travel.vent.on("search:noflightsfound", function(tripsViewObj) {
        // searchQuery against travel agencies done, now show them
	tripsViewObj.destroyView();
        Travel.mainRegion.show(new NoFlightsFoundView());
	
    });


    var app_router = new MyRouter();
    Backbone.history.start();
});

$(document).ready(function(){
    Travel.start();
});
