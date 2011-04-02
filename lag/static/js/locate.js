
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
    window.console.log(lat);
    window.console.log(lon);
    $.post('/locations/a/checkin/',
           {lat: lat, lon:lon},
           function(data){
               window.checkin = $.parseJSON(data);
               window.console.log(data);
           }
          );
}

/** oops */
function geo_error(  ){
    window.console.log("Fail")
}

if (geo_position_js.init()) {
  geo_position_js.getCurrentPosition(geo_success, geo_error);
}
