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
        }
    }

    // Ruin user expectations
    document.addEventListener('touchmove', function(e){e.preventDefault()}, false)

    // Init event bindings
    $(document).ready(LAG.domReady)
    LAG.addLoad(LAG.bodyLoaded)
}())