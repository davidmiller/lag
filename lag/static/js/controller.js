//
// controller.js
//
// Author Barney Carroll <barney.carroll at gmail.com>
// Author David Miller <david at deadpansincerity.com>
//
// LAG prototype application layer
//
// Modify jQuery's AJAX methods to allow us to pass the CSRF hash as a
// request header.
//
// Bind js utility functions to _
//
// Bing application object to LAG
//

// XHR

$('html').ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        // Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});


(function(undefined){
    // Generic utility belt
    _ = {

        // Push to a log in the DOM. Should be invoked as follows for performance:
        // _.debug && _.debug.log('hello devs')
        debug: (function(){

            // Set debug mode via a hash query eg www.some.thing/#debug&whatever
            if(/\bdebug\b/.test(location.hash)) return false

            // Create a DOM object for the log & a method for creating entries
            var entries = $('ul.debugLog').appendTo('body'),
                enter = function(x){
                    return '<li' + (x[1] ? ' class="error"' : '') + '>' + x[0] + '</li>'
                },
                entry

            // Try the expression, log results, append to DOM
            return function log(x){
                try{
                    entry=enter(x)
                }
                catch(e){
                    entry=enter(e,true)
                }

                entries.append(entry)
            }
        }()),

        // If x isn't already an array, make it one with its previous self
        // as the only child. Usefull for loops through +=1 objects.
        arrayify: function(x){
            return $.isArray(x) ? x : [x]
        },

        // Bind events the other way round.
        // {result} takes functions, {cause} takes arrays of format:
        // [{elements}[selector string],{events}[string],{unbind}[optional,boolean]]
        // {result} is bound or unbound to the elements & respective events provided
        resultingFrom: function(result,cause){
            result = _.arrayify(result)
            cause = _.arrayify(cause)

            $.each(cause,function(i,x){
                $.each(result,function(i,y){
                    if(link = x[2])
                        $(x[0]).unbind(x[1],y)
                    else
                        $(x[0]).bind(x[1],y)
                })
            })
        }
    }


    // Extend jQuery
    $.fn.extend({

        // Init, live config & unbinding of iScroll (touchscroll) via $
        // (instead of storing iScroll instances somewhere arbitrary)
        iScroll: function(){
            var THIS = this,
                args = Array.prototype.slice.call(arguments),
                methods = [
                    'destroy',
                    'refresh',
                    'scrollTo',
                    'scrollToElement',
                    'scrollToPage'
                ]

            THIS.each(function(){
                if(!this.iScroll){
                    this.iScroll = new iScroll.apply(
                        null, args.concat(Array.prototype.slice.call(arguments))
                    )
                }
            })

            $.each(methods,function(i,x){
                methods[i] = function(){
                    THIS.each(function(){
                        this.iScroll.apply(
                            null, args.concat(Array.prototype.slice.call(arguments))
                        )
                    })
                }
            })

            return methods
        }
    })


    // Esoteric application object
    LAG = {
        // Container for any previous geolocation checkins
        checkins: [],

        // Stack events to trigger on window.onload
        addLoad: function(fn){

            // The old onload
            var stack = window.onload instanceof Function ?
                window.onload : function(){}
            window.onload = function(){
                fn(),
                stack()
            }
        },

        // Give us 100% width and height, once meta-DOM has reacted to whatever
        resetViewport: function(){
            setTimeout(function(){
                window.scrollTo(0,0)
                console.log('bang')
            },200)
        },

        // iOS Safari keeps the status bar visible until end of load
        bodyLoaded: function(){
            LAG.resetViewport()
        },

        // Every time you push something onto the DOM, you have to refresh
        // iscroll. Let's do that.
        domAlter: function(fn){
            fn();
            setTimeout(function (){
                LAG.contentScroll.refresh();
            }, 0);
            // Probably not the greatest interaction model later, but
            // works for now, & is better than not scrolling back up.
            LAG.contentScroll.scrollTo(0, 0, 200);
        },


        // The big init
        domReady: function(){

            // Touch-scroll for content
            LAG.contentScroll = new iScroll($('.contentOuterSkin')[0],{hScroll: false})
            // Make sure user doesn't screw up the UI
            _.resultingFrom(
                LAG.resetViewport,[
                    [document,'touchmove'],
                    [window,'onresize'],
                    [window,'onorientationchange']
                ]
            )

            // Automatic initial geolocation communication
            LAG.checkin(LAG.initialCheckin);

            // Event binding for interaction events

            // Menu
            $(".icon#artifacts").click( function(){
                LAG.pocket();
                return false;
            });
            $(".icon#location").click( function(){
                LAG.contentPortTo("#visit_details");
                return false;
            });
            $(".icon#gamers").click( function(){
                LAG.contentPortTo("#newsFeed");
                return false;
            });

            // Top menu
            $(".historyCurrent").click( function(){
                LAG.contentPortTo("#places");
                return false;
            });


            // Manual Checkin init
            $("#checkin").click( function(){
                LAG.checkin(LAG.initialCheckin);
                return false;
            });

            // Register a new place
            $("#new").click( function(){
                LAG.newPlace();
                return false;
            });

            // Visit a place
            $(".visit").live("click", function(){
                LAG.visit($(this).attr('id'));
                return false;
            });

            // "Say Yes" to an Item's acquisition model
            $("#acquire_item").live("click", function(){
                LAG.visitAcquire();
                return false;
            });

            // Display the register place form
            $("#showRegisterPlace").click(function(){
                $("#newPlaceForm").css({display: "block"});
                return false;
            });

            // Pickpocket a player
            $(".pickpocket").live("click", function(){
                LAG.pickpocket(this);
                return false;
            });

        },

        // Application Logic


        /** oops */
        vanilla_geo_error: function(){
            LAG.notify("Geolocation not enabled - check your settings");
        },

        // Pretty much every geolocation, we're going to want to store
        // the results.
        checkinSuccess: function(position){
            LAG.lat = position.coords.latitude;
            LAG.lon = position.coords.longitude;
            LAG.acc = position.coords.accuracy;
            LAG.checkin_callback(position);
        },

        //
        // Perform a checkin.
        // Push the current geo data into LAG.checkins if any exists.
        // Then perform the `success` fn.
        // If an error occurs, call the optional `fail` fn, or
        // `vanilla_geo_error`
        //
        checkin: function(success, fail){
            if( LAG.lat && LAG.lon && LAG.acc){
                LAG.checkins.push({lat:LAG.lat, lon:LAG.lon, acc:LAG.acc});
            }
            LAG.checkin_callback = success;
            failure = fail || LAG.vanilla_geo_error;
            // These are from one of the geolocation js libs
            if (geo_position_js.init()) {
                geo_position_js.getCurrentPosition(LAG.checkinSuccess,
                                                   failure);
            }
        },

        // Notify the user of some event for various values of $event
        notify: function(message){
            LAG.domAlter(function(){
                $("#messages").html("");
                if($.isArray(message)){
                    for( var i=0; i < message.length; i++){
                        $("#message_tmpl").tmpl(
                            {message: message[i]}).appendTo("#messages");
                    };
                }else{
                    $("#message_tmpl").tmpl(
                        {message: message}).appendTo("#messages");
                }
            });
        },

        // When we get notifications passed back from the server, we'd
        // like to deal with that, and then pass on whatever else was
        // contained in the JSON
        loads: function(data){
            var json = $.parseJSON(data);
            if ('message' in json){
                LAG.notify(json.message);
                delete json.message;
            }
            return json
        },


        // Generic hide all contentPort
        hideContent: function(){
            LAG.domAlter(function(){
                $("#messages").html("");
                $("#visit_details:visible").hide();
                $("#newsFeed:visible").hide();
                $("#pocket:visible").hide();
                $("#places:visible").hide();
            });
        },

        // Sometimes we'll want to jump to a contentPort div.
        // Take a jquery selector as an arg, hideContent,
        // then show `selector`
        contentPortTo: function(selector){
            LAG.hideContent();
            $(selector).show();
        },

        // on successful geolocation, let's talk to the server and get some
        // local game places.
        initialCheckin: function(position) {
            // Register these as globals so that we can refer to them
            // later without having to make another geolocation call.
            $.post('/locations/checkin/',
                   {lat: LAG.lat, lon: LAG.lon, acc: LAG.acc},
                   function(data){
                       LAG.checkin = LAG.loads(data);
                       LAG.domAlter(function(){
                           $("#lat").text(LAG.lat);
                           $("#lon").text(LAG.lon);
                           $("#acc").text(LAG.acc);
                           $("#nearby_tmpl").tmpl(LAG.checkin.guess).appendTo("#guess");
                           $("#nearby_tmpl").tmpl(LAG.checkin.alternatives).appendTo("#alternatives");
                       });
                   });
        },

        // Interactions:

        // Menu
        pocket: function(){
            LAG.hideContent();
            $.post("/pocket/",
                   function(data){
                       var response = LAG.loads(data);
                       LAG.domAlter(function(){
                           $("#pocketItems").html("");
                           $("#pocketitem_tmpl").tmpl(response.items).appendTo("#pocketItems");
                           $("#pocket").show();
                       });
                   });
        },

        /** Register a new Place */
        newPlace: function(){
            var name = $("input[name='new_place']").val();
            var placetype = $("select#new_placetype']").val();
            $.post("/locations/register-place/",
                   {name: name, lat: LAG.lat, lon: LAG.lon,
                    placetype: placetype},
                   function(data){
                       confirmed_visit_response(data);
                   });
        },

        /** Confirm a visit to a Place already in or database */
        visit: function( place_id ){
            $.post('/locations/visit/',
                   {place_id: place_id},
                   function(data){
                       LAG.visit_details = LAG.loads(data);
                       LAG.domAlter(LAG.parseVisitResponse);
                   });
            // If we're visiting a place, we can probably hide:
            // * the news feed.
            // * the location guesses.
            $("#newsFeed:visible").hide();
            $("#places:visible").hide();
        },

        /** Deal with the json from a confirmed visit */
        parseVisitResponse: function( data ){

            // Let's make sure that visit_details is showing.
            $("#visit_details:hidden").show();
            // Let's clear any previous visit interactions.
            $("#visit_stats").html("");
            $("#visit_npcs").html("");
            $("#visit_item").html("");
            $("#visit_current").html("");

            $(".place").text(LAG.visit_details.stats.name);
            $(".historyCurrent").text(LAG.visit_details.stats.name);
            $("#place_tmpl").tmpl(LAG.visit_details.stats).appendTo("#visit_stats");
            // NPCs
            for(var i=0; i< LAG.visit_details.npcs.length; i++){
                $("#npc_int_tmpl").tmpl(LAG.visit_details.npcs[i]).appendTo("#visit_npcs");
            }
            // Item?
            if(LAG.visit_details.item){
                var item = {
                    name: LAG.visit_details.item.name,
                    flavour_text: LAG.visit_details.item.flavour_text,
                    dilemma: LAG.visit_details.item.acquisition.dilemma,
                    yes: LAG.visit_details.item.acquisition.choices.yes,
                    no: LAG.visit_details.item.acquisition.choices.no
                }
                $("#acquisition_tmpl").tmpl(item).appendTo("#visit_item");
            }

            // Current visitors?
            if(LAG.visit_details.current_visitors){
                $("#visitor_tmpl").tmpl(LAG.visit_details.current_visitors).appendTo("#visit_current");
            }
        },

        // Confirm acquisition of an item that came with a visit
        visitAcquire: function(){
            var callback = LAG.visit_details.item.acquisition.callback;
            $.post(callback.url, callback.params,
                   function(data){LAG.loads(data)});
        },

        // Attempt to pickpocket someone
        pickpocket: function(element){
            var player_id = $(element).attr('player_id');
            $.post('/players/pickpocket/',
                   {player_id: player_id,
                    place_id: LAG.visit_details.stats.id},
                   function(data){
                       LAG.pickpocketing = LAG.loads(data);
                       // Caught!
                       if(!LAG.pickpocketing.result){
                           LAG.domAlter(function(){
                               // TODO remove/alter place we're banned from
                               LAG.contentPortTo("#places");
                               $(".historyCurrent").text("LAG");
                           });
                       }
                       LAG.notify(LAG.pickpocketing.msg);
                   });

        }


    }
    // Ruin user expectations
    document.addEventListener('touchmove', function(e){e.preventDefault()}, false)

    // Init event bindings
    $(document).ready(LAG.domReady)
    LAG.addLoad(LAG.bodyLoaded)
}())