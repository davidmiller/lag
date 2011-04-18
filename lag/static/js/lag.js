//
// lag.js
//
// Author David Miller <david at deadpansincerity.com>
//
// LAG prototype global library functions
//
// Modify jQuery's AJAX methods to allow us to pass the CSRF hash as a
// request header.
//
// Provide site-wide checkin function and client side messages
//

// Shall we have one global variable bucket to not pollute the namespace?
var $lag = {}
$lag.checkins = [];

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

// Notify the user of some event for various values of $event
function notify(message){
    $("#message_tmpl").tmpl({message: message}).appendTo("#messages");
}

// When we get notifications passed back from the server, we'd like to
// deal with that, and then pass on whatever else was contained in the JSON
function json_loads(data){
    var json = $.parseJSON(data);
    if ('message' in json){
        notify(json.message);
        delete json.message;
    }
    return json
}

// Geolocation

/** oops */
function geo_error(){
    notify("Geolocation not enabled - check your settings");
}


// Pretty much every geolocation, we're going to want to store the results.
function checkin_success(position){
    $lag.lat = position.coords.latitude;
    $lag.lon = position.coords.longitude;
    $lag.acc = position.coords.accuracy;
    $lag.checkin_callback(position);
}

//
// Perform a checkin.
// Push the current geo data into $lag.checkins if any exists.
// Then perform the `success` fn.
// If an error occurs, call the optional `fail` fn, or `geo_error`
//
function checkin(success, fail){
    if( $lag.lat && $lag.lon && $lag.acc){
        $lag.checkins.push({lat:$lag.lat, lon:$lag.lon, acc:$lag.acc})
    }
    $lag.checkin_callback = success
    failure = fail || geo_error
        if (geo_position_js.init()) {
            geo_position_js.getCurrentPosition(checkin_success, failure);
        }
}