//
// application.js
//
// Author David Miller <david at deadpansincerity.com>
//
// LAG prototype application
//
// This is currently the entire application. At some stage this will
// likely become unmanageable.
//
// Naming conventions in this file:
//
// Objects:                /[A-Z][a-z]+([A-Z][a-z]+)?/
// Instantiated objects:   /[a-z][a-z]+([A-Z][a-z]+)?/
// Namespaces:             /[a-z]+/
// Constructors:           /initialize/
// Application:            /[A-Z][A-Z]+/
// Top level constants:    /[A-Z][A-Z]+/
//
// Reserved Names:
//
// LAG _ $ __$
//

// Code:

//
// Firstly we provide the esoteric application object.
//
// This has containers that we will fill with our Backbone objects,
// as well as an initialize() function that starts the app.
//

var LAG = {
    // Containers for application components to be inserted into the
    // namespace
    models: {},
    collections: {},
    views: {menu: {}},
    controllers: {},
    // Will hold initialised Models and Collections
    db: {},
    // start the application
    initialize: function(){
        new LAG.controllers.App;
        Backbone.history.start();

    },
}

//
// Models
//
// Here we extend the application object's namespacing with individual models
//

// NewsFeed Items
LAG.models.NewsItem = Backbone.Model.extend({});

// Individual Positions returned from the Geolocation Api
LAG.models.Location = Backbone.Model.extend({

    // We need to send this up the wire, but only the
    // values we actually use server-side
    toPOST: function(){
        return{
            'lat': this.get('latitude'),
            'lon': this.get('longitude'),
            'acc': this.get('accuracy')
        }
    }
});

// Places - Nearby place with basic Place data
LAG.models.Place = Backbone.Model.extend({});

// Items - Held in the pocket
LAG.models.Item = Backbone.Model.extend({});

// Visit related models - will be held as collections in Visit
LAG.models.Visitor = Backbone.Model.extend({});
LAG.models.NPC = Backbone.Model.extend({});

// As far as the JS application is concerned, a VisitItem may as well
// be a seperate model - Acqisition etc is a whole new ballgame
LAG.models.VisitItem = Backbone.Model.extend({});

// In practice this is a singleton class. AFAICT this is fine with Backbone
// as long as you don't do something silly like defining a Collection for it.
LAG.models.Visit = Backbone.Model.extend({
    initialize: function(){
        this.visitors = new LAG.collections.VisitorList;
        this.npcs = new LAG.collections.NPCList;
    },

});

//
// Collections
//
// Provide collections for such models as require them
//
// By convention, collections will be named as either the collective noun
// for it's contents where such a thing makes sense (e.g. Pocket),
// or as ContentList (e.g. PositionList for the model Position).
//
// When overriding fetch(), we are at the minute accessing LAG.db.foo
// by convention, which is possible as we know what singleton pattern
// we'll be using in the application. There is some concern over this.
//

// The Collection we'll loop through to render the NewsFeed
LAG.collections.NewsFeed = Backbone.Collection.extend({
    model: LAG.models.NewsItem,
    url: "/newsfeed",
});


// Hold the Geolocations. We're not using old ones ATM, could very well though
LAG.collections.PositionList = Backbone.Collection.extend({
    model: LAG.models.Location,

    // Async callbacks get handled oddly...
    // We'll assume that window.checkins exists for now.
    checkin: function(success){
        if (geo_position_js.init()) {
            geo_position_js.getCurrentPosition(
                function(position){
                    LAG.db.positions.add([position.coords]);
                    success();
                },
                function(){
                    throw new NotImplementedError(
                        "CheckinList:checkin:failure"
                    );
                });
        }
    }
});

// Nearby Places
LAG.collections.PlaceList = Backbone.Collection.extend({
    model: LAG.models.Place,
    url: '/locations/place',

    // We need to override the initial fetch model, because we're
    // having to post geolocation data to populate the collection.
    // `position` should be an instance of LAG.models.Position
    fetch: function(position){
        $.post('/locations/checkin/',
               position.toPOST(),
               function(data){
                   LAG.db.places.add($.parseJSON(data));
               });
    }
});

// Pocket
LAG.collections.Pocket = Backbone.Collection.extend({
    model: LAG.models.Item,
    url: '/items',

    // Override the standard backbone fetch method
    fetch: function(options){
        var success = options.success || false;
        $.post("/pocket/",
               function(data){
                   var response = $.parseJSON(data);
                   LAG.db.pocket.refresh(response.items);
                   if (success){
                       success();
                   }
               });
    }
});

// Visit related collections
LAG.collections.VisitorList = Backbone.Collection.extend({
    model: LAG.models.Visitor
})

LAG.collections.NPCList = Backbone.Collection.extend({
    model: LAG.models.NPC
})


//
// Views
//

//
// Let's put menus in their own namespace
//


// Location Menu
LAG.views.menu.Location = Backbone.View.extend({
    tagName: "div",
    className: "menu",
    template: $("#locationMenuTmpl"),

    initialize: function(options){
        _.bindAll(this, 'render');
        this.params = options.params;
    },

    render: function(){
        $(this.el).html(this.template.tmpl(this.params));
        $("#LAG").html(this.el);
        return this;
    },

});

// Artifact Menu
LAG.views.menu.Artifact = Backbone.View.extend({
    tagName: "div",
    className: "menu",
    template: $("#artifactMenuTmpl"),

    initialize: function(options){
        _.bindAll(this, 'render');
        this.params = options.params;
    },

    render: function(){
        $(this.el).html(this.template.tmpl(this.params));
        $("#LAG").html(this.el);
        return this;
    },

});


// Generic Views

LAG.views.ModalView = Backbone.View.extend({
    tagname: "div",
    className: "modalItem",
    template: $("#modalTmpl"),

    events: {
        "click .modalOK": "clear"
    },

    initialize: function(options){
        _.bindAll(this, 'render', 'clear');
        this.message = options.message;
    },

    render: function(){
        $(this.el).html(this.template.tmpl({message: this.message}))
        return this;
    },

    clear: function(){
        this.remove();
        return false;
    },

});

//
// Individual views
//

// Display the chrome for the newsfeed (more link etc)
LAG.views.NewsFeed = Backbone.View.extend({
    tagName: "div",
    className: "newsFeed",
    template: $("#newsfeedTmpl"),

    // Take the collection of NewsItems as an option so we can
    // render them as one call in the Controller
    initialize: function(options){
        _.bindAll(this, 'render', 'addNewsItem');
        this.collection = options.collection;
    },

    render: function(){
        $("#LAG").html("");
        $(this.el).html(this.template.tmpl());
        this.collection.each(this.addNewsItem);
        $("#LAG").append(this.el);
        return this;
    },

    addNewsItem: function(item){
        var view = new LAG.views.NewsItem({model: item});
        this.$("#newsItemList").append(view.render().el);
    },
});

// Individual NewsItems
LAG.views.NewsItem = Backbone.View.extend({
    tagName: "div",
    className: "newsItem",
    template: $("#newsitemTmpl"),

    initialize: function(){
        _.bindAll(this, 'render');
    },

    render: function(){
        $(this.el).html(this.template.tmpl(this.model.toJSON()));
        return this;
    },
});

// List of Nearby Places
LAG.views.Nearby = Backbone.View.extend({
    tagName: "div",
    className: "nearby",
    template: $("#nearbyTmpl"),

    // Take a Collection of places from the options
    initialize: function(options){
        _.bindAll(this, 'render', 'addNearbyPlace');
        this.collection = options.collection;
        this.model = options.model;
    },

    // Put the nearby places view in the contentport
    render: function(){
        $("#LAG").html("");
        $(this.el).html(this.template.tmpl(this.model.toJSON()));
        this.collection.each(this.addNearbyPlace);
        $("#LAG").append(this.el);
        return this;
    },

    // Insert a NearbyPlace View
    addNearbyPlace: function(place){
        var view = new LAG.views.NearbyPlace({model: place});
        this.$("#nearbyPlaceList").append(view.render().el);
    },
});

// An individual Place in the NearbyPlaces list
LAG.views.NearbyPlace = Backbone.View.extend({
    tagName: "div",
    className: "nearbyPlace",
    template: $("#nearbyPlaceTmpl"),

    initialize: function(){
        _.bindAll(this, 'render');
    },

    render: function(){
        $(this.el).html(this.template.tmpl(this.model.toJSON()));
        return this;
    },
});

// Place Detail
LAG.views.Place = Backbone.View.extend({
    tagName: "div",
    className: "placeDetail",
    template: $("#placeTmpl"),

    initialize: function(){
        _.bindAll(this, 'render');
    },

    render: function(){
        $("#LAG").html("");
        $(this.el).html(this.template.tmpl(this.model.toJSON()));
        $("#LAG").append(this.el);
        return this;
    },
});

LAG.views.Pocket = Backbone.View.extend({
    tagName: "div",
    className: "pocket",
    template: $("#pocketTmpl"),

    // Take a Collection of items from the options
    initialize: function(options){
        _.bindAll(this, 'render', 'addPocketItem');
        this.collection = options.collection;
    },

    // Put the nearby places view in the contentport
    render: function(){
        $("#LAG").html("");
        $(this.el).html(this.template.tmpl());
        this.collection.each(this.addPocketItem);
        $("#LAG").append(this.el);
        return this;
    },

    // Insert individual PocketItem
    addPocketItem: function(item){
        var view = new LAG.views.PocketItem({model: item});
        this.$("#pocketItemList").append(view.render().el);
    },
});

// View for individual item within a pocket
LAG.views.PocketItem = Backbone.View.extend({
    tagName: "div",
    className: "pocketItem",
    template: $("#pocketItemTmpl"),

    events: {
        "click .moreLess": "moreLess"
    },

    initialize: function() {
        _.bindAll(this, 'render', 'moreLess');
        this.model.bind('change', this.render);
    },

    render: function() {
        $(this.el).html(this.template.tmpl(this.model.toJSON()))
        return this;
    },

    moreLess: function(){
        this.$('.flavour').toggle();
        return false;
    }

});

// Visit related Views

LAG.views.Visit = Backbone.View.extend({
    tagName: "div",
    className: "visit",
    template: $("#visitTmpl"),

    initialize: function(){
        this.visit = LAG.db.visit;
        _.bindAll(this, 'render', 'addNPC');
    },

    render: function(){
        $("#LAG").html("");
        $(this.el).html(this.template.tmpl(this.visit.place.toJSON()));
        this.visit.npcs.each(this.addNPC);
        $("#LAG").append(this.el);
        // Check to see if we have to bring up the modal ItemAcquisition
        // View
        if(LAG.db.visit.item){
            var acquisitionView = new LAG.views.AcquireItemView(
                {model: LAG.db.visit.item}
            );
            $("#modal").html(acquisitionView.render().el);
            delete LAG.db.visit.item;
        }
        return this;
    },

    // Individual View initialization for NPCs
    addNPC: function(npc){
        var view = new LAG.views.VisitNPC({model: npc});
        this.$(".npcList").append(view.render().el);
    },

});

// NPCS at a visit
LAG.views.VisitNPC = Backbone.View.extend({
    tagName: "div",
    className: "visitNPC",
    template: $('#visitNPCTmpl'),

    events: {
        "click .npcInteract": "modalSays"
    },

    initialize: function(){
        _.bindAll(this, 'render', 'modalSays');
    },

    render: function(){
        $(this.el).html(this.template.tmpl(this.model.toJSON()))
        return this;
    },

    // Show whatever the NPC says in a ModalView
    modalSays: function(){
        var view = new LAG.views.ModalView(
            {message: this.model.get('text')}
        );
        $("#modal").html(view.render().el);
    },
});

// Step through the AcquisitionModel for an item
LAG.views.AcquireItemView = Backbone.View.extend({
    tagname: "div",
    className: "modalItem",
    template: $("#acquisitionTmpl"),

    events: {
        "click .sayYes": "sayYes",
        "click .sayNo": "sayNo",
        "click .modalDone": "modalDone",
        "click .acquired": "acquired",
    },

    initialize: function(){
        _.bindAll(this, 'render', 'sayYes', 'sayNo', 'acquired',
                 'modalDone');
    },

    render: function(){
        var item = this.model;
        var params = {
            dilemma: item.acquisition.dilemma,
            yes: item.acquisition.choices.yes,
            no: item.acquisition.choices.no,
            flavour_text: item.flavour_text,
            name: item.name
        }
        $(this.el).html(this.template.tmpl(params))
        return this;
    },

    sayNo: function(){
        this.$('.dilemma').hide();
        this.$('.no').show();
        return false;
    },

    sayYes: function(){
        this.$('.dilemma').hide();
        this.$('.yes').show();
        return false;
    },

    acquired: function(){
        this.$('.yes').hide();
        this.$('.flavourText').show();
        var item = this.model;
        $.post(item.acquisition.callback.url,
               item.acquisition.callback.params);
        return false;
    },

    modalDone: function(){
        this.remove();
        return false;
    },
});


//
// Controllers
//
// The main app controller here
//

LAG.controllers.App = Backbone.Controller.extend({

    routes: {
        "locations": "locationMenu",
        "artifacts": "artifactMenu",
        "newsfeed":  "newsFeed",
        "nearby":    "nearby",
        "place/:id": "place",
        "pocket":    "pocket",
        "visit":     "visit",
        "visit/:id": "visitPlace",
    },

    //
    // It's a big old singleton. Which means that we have to initialize
    // a whole bunch of internal state.
    //
    // Set up the collections in LAG.db
    // Fill them with initial data
    //
    // The total lack of opportunities for dependency injection in this
    // application startup pattern is somewhat worrying.
    //
    initialize: function(){
        _.bindAll(this, 'newsFeed');
        // We want NewsFeed items as the first thing the Player sees.
        LAG.db.newsFeed = new LAG.collections.NewsFeed;
        // Fetch the top # from the server - renders async
        LAG.db.newsFeed.fetch({success: this.newsFeed});
        // Initialize the Geolocation positions Collection
        LAG.db.positions = new LAG.collections.PositionList;
        // Collection for nearby places
        LAG.db.places = new LAG.collections.PlaceList;
        // Get the Player's current position.
        // Once we have it, let's get a list of nearby places.
        LAG.db.positions.checkin(function(){
            LAG.db.places.fetch(LAG.db.positions.last());
        });
        // Every player has a pocket
        LAG.db.pocket = new LAG.collections.Pocket;
        // We'll define a Visit on initialize - because if they don't
        // visit somewhere, then frankly what's the point.
        LAG.db.visit = new LAG.models.Visit;
    },

    // Menus
    locationMenu: function(){
        params = {
            nearby: LAG.db.places.length
        }
        if(LAG.db.visit.place){
            params.visit = LAG.db.visit.place.get('name');
        }
        var menuView = new LAG.views.menu.Location({params: params});
        menuView.render();
    },

    artifactMenu: function(){
        var renderView = function(){
            params = {
                itemCount: LAG.db.pocket.length
            }
            var menuView = new LAG.views.menu.Artifact({params: params});
            menuView.render();
        }
        if(LAG.db.pocket.length == 0){
            LAG.db.pocket.fetch({success: renderView});
        }else{
            renderView();
        }
    },

    newsFeed: function(){
        var newsFeedView = new LAG.views.NewsFeed({
            collection: LAG.db.newsFeed
        });
        newsFeedView.render();
    },

    // Display the view for display nearby places
    nearby: function(){
        var nearbyView = new LAG.views.Nearby({
            collection: LAG.db.places,
            model: LAG.db.positions.first(),
        });
        nearbyView.render();
    },

    // Display the detail for a place
    place: function(id){
        var place = LAG.db.places.get(id);
        var placeView = new LAG.views.Place({model: place});
        placeView.render();
    },

    // What's in your pocket?
    pocket: function(){
        var pocketView = new LAG.views.Pocket({collection: LAG.db.pocket});
        // Get the latest Pocket, then render the items
        LAG.db.pocket.fetch({success: pocketView.render});
    },

    // Show the current visit
    visit: function(){
        var visitView = new LAG.views.Visit({model: LAG.db.visit});
        visitView.render();
    },

    // Visit a place
    visitPlace: function(id){
        LAG.db.visit.place = LAG.db.places.get(id);
        // XHR fetch for a visit
        $.post(
            '/locations/visit/',
            {place_id: id},
            function(data){
                response = $.parseJSON(data);
                // Take Item, npcs, visitors out of the response, store
                // in the model
                if(response.current_visitors){
                    LAG.db.visit.visitors.refresh(
                        response.current_visitors
                    );
                    delete response.current_visitors;
                }
                if(response.npcs){
                    LAG.db.visit.npcs.refresh(response.npcs);
                    delete response.npcs;
                }
                if(response.item){
                    LAG.db.visit.item = response.item;
                    delete response.item;
                }
                // Now we've set the data we can render it
                var visitView = new LAG.views.Visit(
                    {model: LAG.db.visit}
                );
                visitView.render();
            }
        );
    },
});


$(function(){
    LAG.initialize();
});
