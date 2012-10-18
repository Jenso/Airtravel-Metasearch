$.ajaxSetup({
    cache: false
});

Travel = new Backbone.Marionette.Application();

Travel.addRegions({
    mainRegion: "#content"
});

var Trip = Backbone.Tastypie.Model.extend({
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

var TripsCollection = Backbone.Tastypie.Collection.extend({
    urlRoot: TRIPS_API_URL,
    model: Trip,
});

var TripView = Backbone.Marionette.ItemView.extend({
    template: "#tpl-trip",
    className: "trip",
    tagName: "li",
    events: {
        'click': 'tripOverlay',
    },
    tripOverlay: function() {
	//OPEN ME!
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
        this.collection.fetch({
            success: function(collection, response) {
                console.log("ho", collection, response);
            }
        });
    },
    appendHtml: function(collectionView, itemView, index){
        collectionView.$el.find("#search-results").prepend(itemView.el);
    }
});


var SearchView = Backbone.Marionette.ItemView.extend({
    //itemView: PinView,
    template: "#tpl-search-area",
    initialize: function() {

    },
    onRender: function () {
        $.datepicker.regional['sv'] = {
            closeText: 'Stäng',
            prevText: '&laquo;Förra',
            nextText: 'Nästa&raquo;',
            currentText: 'Idag',
            monthNames: ['Januari','Februari','Mars','April','Maj','Juni',
                         'Juli','Augusti','September','Oktober','November','December'],
            monthNamesShort: ['Jan','Feb','Mar','Apr','Maj','Jun',
                              'Jul','Aug','Sep','Okt','Nov','Dec'],
            dayNamesShort: ['Sön','Mån','Tis','Ons','Tor','Fre','Lör'],
            dayNames: ['Söndag','Måndag','Tisdag','Onsdag','Torsdag','Fredag','Lördag'],
            dayNamesMin: ['Sö','Må','Ti','On','To','Fr','Lö'],
            weekHeader: 'Ve',
            dateFormat: 'yy-mm-dd',
            firstDay: 1,
            isRTL: false,
            showMonthAfterYear: false,
            yearSuffix: ''};
        $.datepicker.setDefaults($.datepicker.regional['sv']);

        this.$("#datepicker-arrival").datepicker({firstDay: 1});
        this.$("#datepicker-departure").datepicker({firstDay: 1});
    },
    events: {
        'click #search-trip': 'searchTrip',
    },
    searchTrip: function() {
        console.log("hi");
    },
});

Travel.addInitializer(function(options){
    function trackCategory(category) {
        _kmq.push(['record', 'Changed category', {'Category': category}]);
    }

    MyRouter = Backbone.Marionette.AppRouter.extend({
        routes : {
            "sök" : "search",
            "*actions": "defaultRoute",
        },
        search: function() {
            var trips = new TripsCollection();
            var TripsView1 = new TripsView({
                collection: trips,
            });

            Travel.mainRegion.show(TripsView1);

        },
        defaultRoute: function() {
            //var collection = new PinsPagerCollection();
            var SearchView1 = new SearchView({
            });

            Travel.mainRegion.show(SearchView1);

        },
    });
    var app_router = new MyRouter();
    Backbone.history.start();
});

$(document).ready(function(){
    Travel.start();
});
