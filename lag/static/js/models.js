//
// mdoels.js
//
// Author David Miller <david at deadpansincerity.com>
//
// LAG prototype models
//
// Establish our models and collections for LAG
//

// Start with individual Positions
var Location = Backbone.Model.extend({
    toPOST: function(){
        return{
            'lat': this.get('latitude'),
            'lon': this.get('longitude'),
            'acc': this.get('accuracy')
        }
    }
});

// Now we want somewhere to hold the Geolocations
var CheckinList = Backbone.Collection.extend({
    model: Location,

    // Async callbacks get handled oddly...
    // We'll assume that window.checkins exists for now.
    checkin: function(){
        if (geo_position_js.init()) {
            geo_position_js.getCurrentPosition(
                function(position){
                    checkins.add([position.coords]);
                    places.fetch();
                },
                function(){
                    throw new NotImplementedError(
                        "CheckinList:checkin:failure"
                    );
                });
        }
    }
});

//
// Now we'll deal with Places.
//
// Some places (ones we're visiting) will have NPCS and Visitors
//

var Visitor = Backbone.Model.extend({});
var VisitorList = Backbone.Collection.extend({
    model: Visitor
})

var NPC = Backbone.Model.extend({});
var NPCList = Backbone.Collection.extend({
    model: NPC
})


var Place = Backbone.Model.extend({
    initialize: function(){
        this.visitors = new VisitorList;
        this.npcs = new NPCList;
    },

    // For each place, we should be able to fetch the
    // NPCs / item / visitors for a fresh visit to that place.
    fetchVisit: function(){
        // Some esoteric aspect of js scoping requires us to
        // declare callbacks like this.
        // Taking lead from Backbone.Model.fetch
        var model = this;
        var success = function(data){
            visit_data = LAG.loads(data)
            // If we have NPCs or visitors, refresh the nested
            // Collection
            if(visit_data.current_visitors){
                model.visitors.refresh(visit_data.current_visitors);
            }
            if(visit_data.npcs){
                model.npcs.refresh(visit_data.npcs);
            }
            if(visit_data.item){
                model.set({item: visit_data.item});
            }
        }
        // Perform the XHR fetch
        $.post(
            '/locations/visit/',
            {place_id: this.get('id')},
            success
        );
        return this;
    },
});

var PlaceList = Backbone.Collection.extend({
    model: Place,
    url: '/locations/place',

    // We need to override the initial fetch model, because we're
    // having to post geolocation data to populate the collection.
    fetch: function(){
        position = checkins.first();
        $.post('/locations/checkin/',
               position.toPOST(),
               function(data){
                   places.add($.parseJSON(data));
               });
    }

});

// Time for items now

var Item = Backbone.Model.extend({});

var Pocket = Backbone.Collection.extend({
    model: Item,
    url: '/items',

    // Override the standard backbone fetch method
    fetch: function(){
        $.post("/pocket/",
               function(data){
                   var response = LAG.loads(data);
                   pocket.refresh(response.items);
               });
    }
});
