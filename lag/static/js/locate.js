//
// locate.js
//
// Author David Miller <david at deadpansincerity.com>
//
// LAG project homepage prototype
//
// By nature this file is mostly DOM munging and
// registering handlers for various events.
//
// We will also modify jQuery's AJAX
// methods to allow us to pass the CSRF hash as a
// request header.
//

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

// On successful geolocation, let's talk to the server and get some
// local game places.
function geo_success(position) {
    // Register these as globals so that we can refer to them
    // later without having to make another geolocation call.
    window.lat = position.coords.latitude;
    window.lon = position.coords.longitude;

    $.post('/locations/checkin/',
           {lat: window.lat, lon: window.lon},
           function(data){
               var checkin = $.parseJSON(data);
               // Register the server response as a global.
               window.checkin = checkin
               var alternat_holder = $("#alternatives");
               $("#lat").text(window.lat);
               $("#lon").text(window.lon);
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

/** oops */
function geo_error(){
    $("#response").append("<p>Geolocation not enabled - check your settings</p>");
}

/** Register a new Place */
function register_new( name ){
    $.post("/locations/register-place/",
           {name: name, lat: window.lat, lon: window.lon},
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
    window.visit_details = $.parseJSON(data);
    $(".place").text(window.visit_details.name);
    var stats_div = $("#visit_stats");
    $(stats_div).append("<p>Created by: "+window.visit_details.created_by+"</p>");
    $(stats_div).append("<p>This is your: "+window.visit_details.player_visit_count+"th visit</p>");
}

$(document).ready( function(){
    // Manual Checkin init
    $("#checkin").click( function(){
        if (geo_position_js.init()) {
            geo_position_js.getCurrentPosition(geo_success, geo_error);
        }else{
            no_geo()
        }
    });

    // Register a new place
    $("#new").click( function(){
        var name = $("input[name='new_place']").val();
        register_new(name);
    });

    // Confirm our suggestion
    $("#confirm_guess").click( function(){
        confirm_visit(window.checkin.guess[0]);
    });

    // Confirm one of the alternatives
    $(".confirm_alt").live("click", function(){
        confirm_visit($(this).attr('id'));
    });
});

