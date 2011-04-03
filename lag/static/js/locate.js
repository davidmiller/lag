
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

// let's show a map or do something interesting!
function geo_success(position) {
    var lat = position.coords.latitude;
    var lon = position.coords.longitude
    $.post('/locations/a/checkin/',
           {lat: lat, lon:lon},
           function(data){
               window.checkin = $.parseJSON(data);
               var place = window.checkin.place;
               var creator = window.checkin.creator;
               var visit_count = window.checkin.visit_count;
               var last_visited = window.checkin.last_visited;
               var target = $("#response")
               $(target).append("<p>You are at lat:"+lat+", lon:"+lon+"</p>");
               $(target).append("<p>We think this place is called "+place+"</p>");
               $(target).append("<p>We think that this place was created by "+creator+"</p>");
               $(target).append("<p>You have visited this place "+visit_count+" times</p>");
               $(targed).append("<p>You last visited on "+last_visited+"</p>");
               $
           }
          );
}

/** oops */
function geo_error(  ){

    $("#response").append('<p> Sorry, no geo</p>');
}

if (geo_position_js.init()) {
  geo_position_js.getCurrentPosition(geo_success, geo_error);
}
