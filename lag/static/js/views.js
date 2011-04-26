//
// views.js
//
// Author David Miller <david at deadpansincerity.com>
//
// LAG prototype views
//
// Establish the views for each model and then the interaction based ones.
// AppView is the top level UI element.
//



// Generic Views - Modal

var ModalView = Backbone.View.extend({
    tagname: "div",
    className: "modalItem",
    template: $("#modal_tmpl"),

    events: {
        "click .modalOK": "clear"
    },

    initialize: function(message){
        _.bindAll(this, 'render', 'clear');
        this.message = message;
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

// Visit related views

var NPCView = Backbone.View.extend({
    tagName: "div",
    className: "VisitNPC",
    template: $('#npc_int_tmpl'),

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

    modalSays: function(){
        var view = new ModalView(this.model.get('text'))
        $("#modal").html(view.render().el);
    },

});

var AcquireItemView = Backbone.View.extend({
    tagname: "div",
    className: "modalItem",
    template: $("#acquisition_tmpl"),

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
        var item = this.model.get('item');
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
        var item = this.model.get('item');
        $.post(item.acquisition.callback.url,
               item.acquisition.callback.params);
        return false;
    },

    modalDone: function(){
        this.remove();
        return false;
    },
});

var VisitView = Backbone.View.extend({
    tagName: "div",
    className: "visitDetails",
    template: $("#visit_tmpl"),

    initialize: function() {
        // FFS - always run the render function with a scope that's
        // not insane.
        _.bindAll(this, 'render', 'addNPC', 'refreshNPCS', 'changeItem'),
        // Re-render when the model changes
        this.model.bind('refresh', this.render);
        this.model.npcs.bind('refresh', this.refreshNPCS);
        this.model.bind('change:item', this.changeItem);
    },

    render: function() {
        $(this.el).html(this.template.tmpl(this.model.toJSON()))
        return this;
    },

    refreshVisit: function(){
        throw new NotImplementedError("visitView:refreshVisit");
    },

    // NPCS for visit
    addNPC: function(npc) {
        var view = new NPCView({model: npc});
        this.$('.npcs').append(view.render().el);
    },

    refreshNPCS: function(){
        this.$('.npcs').html('');
        this.model.npcs.each(this.addNPC);
    },

    // Visit Item
    changeItem: function(place){
        var view = new AcquireItemView({model: place});
        this.$('.item').html(view.render().el);
    }


});


var PlaceView = Backbone.View.extend({
    tagName: "div",
    className: "place",
    template: $("#place_tmpl"),

    events: {
        "click .moreLess": "moreLess",
        "click .visit": "visit"
    },

    initialize: function() {

        // FFS - always run the render function with a scope that's
        // not insane.
        _.bindAll(this, 'render'),
        this.visitView = new VisitView({model: this.model});
        this.model.bind('change', this.render);
    },

    render: function() {
        $(this.el).html(this.template.tmpl(this.model.toJSON()))
        return this;
    },

    // Toggling the stats/list display
    moreLess: function(){
        this.$('.placeStats').toggle();
        return false;
    },

    visit: function(){
        LAG.$("#visit").html(this.visitView.render().el)
        this.model.fetchVisit();
        LAG.contentPortTo('#visit');
        return false;
    }

});

var ItemView = Backbone.View.extend({
    tagName: "div",
    className: "pocketItem",
    template: $("#pocketitem_tmpl"),

    events: {
        "click .moreLess": "moreLess"
    },

    initialize: function() {
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

//
// Main App view
//

var LagView = Backbone.View.extend({

    el: $(".bodyOuterSkin"),

    events: {
        "click .icon#artifacts": "artifactsMenu",
        "click .icon#locationsMenu": "locationsMenu",
        "click .historyCurrent": "nearbyMenu"
    },

    initialize: function(){
        _.bindAll(this, 'render');
        places.bind('add', this.addPlace);
        pocket.bind('add', this.addToPocket);
        pocket.bind('refresh', this.refreshPocket);
        checkins.checkin();
    },

    render: function(){

    },


    // Utilities

    loads: function(data){
        return $.parseJSON(data);
    },

    // Sometimes we'll want to jump to a contentPort div.
    // Take a jquery selector as an arg, hideContent,
    // then show `selector`
    contentPortTo: function(selector){
        $(".contentInnerSkin").children().hide();
        $(selector).show();
        return false;
    },

    //
    // Top level adding of places to placeList and items to pocket
    //

    addPlace: function(place){
        var view = new PlaceView({model: place});
        LAG.$("#placeList").append(view.render().el);
    },

    addToPocket: function(item){
        var view = new ItemView({model: item});
        LAG.$("#pocket").append(view.render().el);
    },

    refreshPocket: function(item){
        LAG.$("#pocket").html("");
        pocket.each(LAG.addToPocket);
    },

    // Menu interactions
    artifactsMenu: function(){
        pocket.fetch()
        return LAG.contentPortTo('#pocket');
    },

    locationsMenu: function(){
        return LAG.contentPortTo('#locationsMenu');
    },

    nearbyMenu: function(){
        return LAG.contentPortTo('#placeList');
    },
});
