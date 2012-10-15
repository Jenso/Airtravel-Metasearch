$.ajaxSetup({
    cache: false
});

Travel = new Backbone.Marionette.Application();

Travel.addRegions({
    mainRegion: "#content"
});


var TravelCollection = Backbone.Collection.extend({
    url: '/api/travel/',
});

var TripView = Backbone.Marionette.ItemView.extend({
    template: "#tpl-trip",
    className: "trip",
    tagName: "li",
    events: {
        'click': 'pinOverlay',
    },
    pinOverlay: function() {
        var pinOverlay = new PinOverlayView({model: this.model}).render();
        // FIXME: is this really a good way to add it to the div?
        this.$el.append(pinOverlay.$el);
    },
});


var TripsView = Backbone.Marionette.CollectionView.extend({
    itemView: TripView,
    tagName: "ul",
    initialize: function() {
    },
});

var SearchView = Backbone.Marionette.ItemView.extend({
    //itemView: PinView,
    template: "#tpl-search-area",
    initialize: function() {

    },
    events: {
	'click #search-trip': 'searchTrip',
    },
    searchTrip: function() {
	console.log("hi");
    },
});


var Trip = Backbone.Model.extend({});

var TripsCollection = Backbone.Collection.extend({
  model: Trip,
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
	    var cats = new TripsCollection([
		new Trip({ name: 'Wet Cat', image_path: 'assets/images/cat2.jpg' }),
		new Trip({ name: 'Bitey Cat', image_path: 'assets/images/cat1.jpg' }),
		new Trip({ name: 'Surprised Cat', image_path: 'assets/images/cat3.jpg' })
	    ]);
	    var TripsView1 = new TripsView({
		collection: cats,
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
