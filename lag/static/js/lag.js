//
// lag.js
//
// Author Barney Carroll <barney.carroll at gmail.com>
// Author David Miller <david at deadpansincerity.com>
//
// LAG prototype global library functions.
//
// The contents of this file are not application specific in terms
// of logic, DOM or data manipulation.
//
// Configuration/alteration of jQuery on an app-global state, for the
// initialisation of js-based scrolling and CSRF XHR headers.
//
// Utility functions bound to __$
//
// Also - let's have js Error Classes!
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
                    cookieValue = decodeURIComponent(
                        cookie.substring(name.length + 1)
                    );
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
    __$ = {

        // Push to a log in the DOM. For performance, should be invoked::
        // __$debug && __$debug.log('hello devs')
        debug: (function(){

            // Set debug mode via a hash query eg www.some.thing/#debug&hai
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
        // [{elements}[selector string],{events}[string],
        // {unbind}[optional,boolean]]
        // {result} is bound or unbound to the elements & respective
        // events provided
        resultingFrom: function(result,cause){
            result = __$arrayify(result)
            cause = __$arrayify(cause)

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
                        null, args.concat(
                            Array.prototype.slice.call(arguments)
                        )
                    )
                }
            })

            $.each(methods,function(i,x){
                methods[i] = function(){
                    THIS.each(function(){
                        this.iScroll.apply(
                            null, args.concat(
                                Array.prototype.slice.call(arguments)
                            )
                        )
                    })
                }
            })

            return methods
        }
    })
    // Ruin user expectations
    document.addEventListener('touchmove',
                              function(e){e.preventDefault()}, false)


}())


// Let's behave nicely for certain classes of error
function NotImplementedError(feature){
    this.name = "NotImplementedError",
    this.message = feature || "This feature";
}
NotImplementedError.prototype = Error.prototype;
