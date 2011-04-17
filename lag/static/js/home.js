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
                   alt_p += checkin.alternatives[i][0]+'">Confirm</a></p><hr />';
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
function visit( place_id ){
    $.post('/locations/visit/',
           {place_id: place_id},
           function(data){
               parse_visit_response(data);
           });
}

/** Deal with the json from a confirmed visit */
function parse_visit_response( data ){
    $lag.visit_details = json_loads(data);
    $(".place").text($lag.visit_details.name);
    $("#visit_stats").html("");
    $("#visit_npcs").html("");
    $("#visit_item").html("");
    $("#place_tmpl").tmpl($lag.visit_details.stats).appendTo("#visit_stats");
    // NPCs
    for(var i=0; i< $lag.visit_details.npcs.length; i++){
        $("#npc_int_tmpl").tmpl($lag.visit_details.npcs[i]).appendTo("#visit_npcs");
    }
    // Item?
    if($lag.visit_details.item){
        var item = {
            name: $lag.visit_details.item.name,
            flavour_text: $lag.visit_details.item.flavour_text,
            dilemma: $lag.visit_details.item.acquisition.dilemma,
            yes: $lag.visit_details.item.acquisition.choices.yes,
            no: $lag.visit_details.item.acquisition.choices.no
        }
        $("#acquisition_tmpl").tmpl(item).appendTo("#visit_item");
    }
}

$(document).ready( function(){

    // Automatically get location
    checkin(homepage_checkin)

    // Manual Checkin init
    $("#checkin").click( function(){
        checkin(homepage_checkin);
        return false;
    });

    // Register a new place
    $("#new").click( function(){
        var name = $("input[name='new_place']").val();
        register_new(name);
        return false;
    });

    // Confirm our suggestion
    $("#confirm_guess").click( function(){
        visit($lag.checkin.guess[0]);
        return false;
    });

    // Confirm one of the alternatives
    $(".confirm_alt").live("click", function(){
        visit($(this).attr('id'));
        return false;
    });
});

