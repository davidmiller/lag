//
// lair.js
//
// Author David Miller <david at deadpansincerity.com>
//
// LAG prototype Lair interaction
//
// Some Lair specific api calls.
//

// Get the player's geolocation coordinates.
// Pass them and the name to the API
function create_lair(position){
    var name = $("#new_name").val();
    $.post(window.location.pathname,
           {lat: $lag.lat,
            lon: $lag.lon,
            name: name},
           function(data){
               var lair_data = json_loads(data);
               $("#lair_tmpl").tmpl(lair_data).appendTo("#lair_detail");
               $("#lair_create").remove();
           })
}


// Bind functions to hrefs
$(document).ready( function(){
    // Manual Checkin init
    $("#create_lair").click( function(){
        checkin(create_lair);
    });
});