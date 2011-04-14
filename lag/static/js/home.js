//
// home.js
//
// Author David Miller <david at deadpansincerity.com>
//
// LAG project homepage prototype
//
// By nature this file is mostly DOM munging and
// registering handlers for various events.
//


// On successful geolocation, let's talk to the server and get some
// local game places.
function homepage_checkin(position) {
    // Register these as globals so that we can refer to them
    // later without having to make another geolocation call.
    $.post('/locations/checkin/',
           {lat: $lag.lat, lon: $lag.lon},
           function(data){
               var checkin = $.parseJSON(data);
               // Register the server response as a global.
               $lag.checkin = checkin
               var alternat_holder = $("#alternatives");
               $("#lat").text($lag.lat);
               $("#lon").text($lag.lon);
               $("#acc").text($lag.acc);
               $("#guess").text(checkin.guess[1]);

               for( var i=0; i < checkin.alternatives.length; i++){
                   var alt_p = "<p>"+checkin.alternatives[i][1]+"<p>";
                   alt_p += '<p><a href="#" class="confirm_alt" id="';
                   alt_p += checkin.alternatives[i][0]+'">Confirm</a></p>';
                   $(alternat_holder).append(alt_p);
               }
               $
           }
          );
}


/** Register a new Place */
function register_new( name ){
    $.post("/locations/register-place/",
           {name: name, lat: $lag.lat, lon: $lag.lon},
           function(data){
               confirmed_visit_response(data);
           });
}

/** Confirm a visit to a Place already in or database */
function confirm_visit( place_id ){
    $.post('/locations/confirm-visit/',
           {place_id: place_id},
           function(data){
               confirmed_visit_response(data);
           });
}

/** Deal with the json from a confirmed visit */
function confirmed_visit_response( data ){
    $lag.visit_details = $.parseJSON(data);
    $(".place").text($lag.visit_details.name);
    var stats_div = $("#visit_stats");
    $(stats_div).append("<p>Created by: "+$lag.visit_details.created_by+"</p>");
    $(stats_div).append("<p>This is your: "+$lag.visit_details.player_visit_count+"th visit</p>");
}

$(document).ready( function(){
    // Manual Checkin init
    $("#checkin").click( function(){
        checkin(homepage_checkin);
    });

    // Register a new place
    $("#new").click( function(){
        var name = $("input[name='new_place']").val();
        register_new(name);
    });

    // Confirm our suggestion
    $("#confirm_guess").click( function(){
        confirm_visit($lag.checkin.guess[0]);
    });

    // Confirm one of the alternatives
    $(".confirm_alt").live("click", function(){
        confirm_visit($(this).attr('id'));
    });
});

