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
    url: "http://localhost:8888",
    model: Trip,
});

var AirportsCollection = Backbone.Tastypie.Collection.extend({
    url: AIRPORTS_API_URL,
});

var AirportView = Backbone.Marionette.ItemView.extend({
});

var AirportSearchView = Backbone.Marionette.CompositeView.extend({
    itemView: AirportView,
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
    events: {
        'click': 'tripOverlay',
    },
    tripOverlay: function() {
        console.log(this.model);
    },
    parseDate: function(str) {
        //YYYYmmdd or YYYY-mm-dd

        // remove all non digits
        str = str.replace(/\D/g,'');
        var y = str.substr(0,4),
        m = str.substr(4,2) - 1,
        d = str.substr(6,2);
        var D = new Date(y,m,d);
        return (D.getFullYear() == y && D.getMonth() == m && D.getDate() == d) ? D : 'invalid date';
    },

});


var TripsView = Backbone.Marionette.CompositeView.extend({
    itemView: TripView,
    template: "#tpl-trips",
    tagName: "div",
    className: "search-result-list",
    initialize: function() {
    },
    appendHtml: function(collectionView, itemView, index){
        collectionView.$el.find("#search-results").append(itemView.el);
    }
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
	//_.bindAll(this, 'getQuickselectData');
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
            changeMonth:true,
            changeYear: true,
            showOtherMonths:true,
            selectOtherMonths:true,
            showWeek:true,
            yearSuffix: ''};
        $.datepicker.setDefaults($.datepicker.regional['sv']);
        var _this = this;
        this.$("#datepicker-departure-date").datepicker({firstDay: 1,
        											onSelect: function(dateText, inst){
	        											_this.departureDateFromDatepicker =  dateText;
        											}
        											
        											});
        this.$("#datepicker-return-date").datepicker({firstDay: 1,
                                                    onSelect: function(dateText, inst) {
                                                    	_this.arrivalDateFromDatepicker = dateText;
                                                    }

                                                   });
	this.initQuickselect();
    },
    events: {
        'click #search-trip': 'searchTrip',
        'click #trip-type' : 'hideArrivalDate' 
    },
    initQuickselect: function() {
	//this.$('input#from').quickselect({data: ['option1', 'option2', 'option3']});
	var options = {ajax: "http://localhost:8888/airports/", minChars: 2};
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
    	
    	var date1 = isNaN(parsedDate1);
    	var date2 = isNaN(parsedDate2);
    
	    if (isNaN(parsedDate1) && isNaN(parsedDate2)){
	    	alert("Var god och välj datum för din resa.")
		    return 2;
	    }
	    else if (isNaN(parsedDate1)){
	    	alert("Var god och välj datum för din utresa.")
		    return 3;
	    }
	    else if (isNaN(parsedDate2)){
	    	if(this.$('#trip-type').attr('checked')){
		    	return 0;
	    	}
	    	else{
	    		alert("Var god och välj datum för din hemresa.")
	    		return 4;
	    	}
	    }
	    else{
		    null;
	    }
    },	
    
    dateValidation: function(date1, date2){
    	var d1 = Date.parse(date1);
    	var d2 = Date.parse(date2);
    	if (d2 >= d1){
			return 0;
		}
	    else if (d2 < d1){
	    	alert("Ditt datum för utresa ligger efter ditt datum för hemresa, var god försök igen :) ");
		    return 1;
	    }
	    else{
		    return this.testNaN(d1, d2);
	    }
    },

    searchTrip: function() {
	if(this.$('#trip-type').attr('checked')) {
	    var tripType = 'ONEWAY';
	} else {
	    var tripType = 'ROUNDTRIP';
	}
        var searchParams = {
            'tripType': tripType,
            'departureIata': this.extractIata(this.$('input#from').val()),
            'arrivalIata': this.extractIata(this.$('input#to').val()),
            "departureDate": this.departureDateFromDatepicker,
            "returnDate": this.arrivalDateFromDatepicker,
            "ticketType":"ECONOMY",
            "adults": this.$('#number-adults').val(),
            "children": this.$('#number-children').val(),
            "infants":"0",
        };
    
        var dateTest = this.dateValidation(searchParams.departureDate, searchParams.returnDate);
        console.log(dateTest);
        if (dateTest == 0){
        	console.log("begin search");
	        Travel.vent.trigger("search:start", searchParams);
        }
        else if (dateTest == 1){
        }
        else{
	        console.log("Please enter");
        };
        
    },
    
    hideArrivalDate: function(){
    	this.$('#label-to-return-date').toggle();
    	this.$('#datepicker-return-date').toggle();
	}, 
    
});

Travel.addInitializer(function(options){
    function trackCategory(category) {
        _kmq.push(['record', 'Changed category', {'Category': category}]);
    }

    MyRouter = Backbone.Marionette.AppRouter.extend({
        routes : {
            "test-search" : "search",
            "*actions": "defaultRoute",
        },
        search: function() {
	    var test_data =  {
                'tripType':'ROUNDTRIP',
                'departureIata': 'CPH',
                'arrivalIata': 'NCE',
                "departureDate":"2012-11-01",
                "returnDate":"2012-11-06",
                "ticketType":"ECONOMY",
                "adults":"1",
                "children":"0",
                "infants":"0",
            };

	    Travel.vent.trigger("search:start", test_data);

        },
        defaultRoute: function() {
        
        
        
            //var collection = new PinsPagerCollection();
            var SearchView1 = new SearchView();

            Travel.mainRegion.show(SearchView1);

        },
    });


    Travel.vent.on("search:start", function(searchTerm){
	Travel.mainRegion.show(new WaitingSearchView());

	var trips = new TripsCollection();

	$.ajax({
	    url: AIRPORTS_API_URL,
	    //data: "iata__in=" + searchTerm.departureIata + "&iata__in=" + searchTerm.arrivalIata,
	    data: "iata__in=" + "ARN" + "&iata__in=" + "JFK",
            success: function (response) {
		console.log("rrr",response);
            }
	});

        trips.fetch({
	    data: searchTerm,
            success: function(collection, response) {
		Travel.mainRegion.show(
		    new TripsView({
			collection: collection,
		    })
		);

                console.log("ho", collection, response);
            }
        });

        //Backbone.history.navigate("search/" + searchTerm);
        console.log(searchTerm);
    });

    var app_router = new MyRouter();
    Backbone.history.start();
});

$(document).ready(function(){
    Travel.start();
});
