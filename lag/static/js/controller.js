
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
