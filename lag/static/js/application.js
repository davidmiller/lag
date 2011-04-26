//
// bone.js
//
// Author David Miller <david at deadpansincerity.com>
//
// LAG prototype application initialisation
//
// This finally initialises the application - put instances into the
// global namespace.
//

$(function(){
    window.checkins = new CheckinList;
    window.places = new PlaceList;
    window.pocket = new Pocket;
    window.LAG = new LagView;
});
