"""
Let's get viewtastic with our players
"""

import json

from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from django.http import HttpResponseRedirect, HttpResponse

from lag.items.models import Pickpocketing
from lag.items.pickpocket import pickpocketing
from lag.locations.models import Lair, PlaceType, Place
from lag.news.models import news_feed
from lag.players.forms import PlayerForm
from lag.players.models import Player
from lag.utils.shortcuts import render_to

@render_to('players/home.html')
def home(request):
    """
    Let's see what we do with this user...

    Arguments:
    - `req`:
    """
    try:
        player = request.user.get_profile()
    except AttributeError:
        return HttpResponseRedirect("/")
    newsfeed = news_feed(player)
    placetypes = PlaceType.objects.all()
    return dict(player=player, placetypes=placetypes, newsfeed=newsfeed)

@login_required
@render_to('players/edit_profile.html')
def edit_profile(request):
    """
    Change yer profile

    Arguments:
    - `request`: HttpRequest
    """
    player = request.user.get_profile()
    if request.method == 'POST':
        form = PlayerForm(request.POST, request.FILES, instance=player)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/home/')
    else:
        form = PlayerForm(instance=player)
    return dict(form=form, player=player)

@login_required
@render_to('players/lair_detail.html')
def lair_detail(request):
    """
    If the player has a lair set, then they have the opportunity to
    perform various Lair-specific interactions.

    Otherwise, they can set their lair.
    """
    player = request.user.get_profile()
    if request.method == "POST":
        lat = request.POST['lat']
        lon = request.POST['lon']
        name = request.POST['name']
        point = Point(x=float(lon), y=float(lat))

        lair = Lair(lat=lat, lon=lon, created_by=player,
                    point=point,
                    name=name)
        lair.save()

        player.lairs.add(lair)
        player.has_lair = True
        player.save()
        created = lair.created.strftime("%Y-%m-%d")
        msg = "You've just created your lair - have some objectz"


    else:
        lairqs = player.lairs.filter(active=True)

        if lairqs.count() == 0:
            return dict(player=player)
        lair = lairqs[0]
        name = lair.name
        created = lair.created.strftime("%Y-%m-%d")

    if request.is_ajax():
        return HttpResponse(json.dumps(dict(name=name, created=created,
                                            message=msg)))
    return dict(player=player, name=name,
                created=created, lair=lair)
@login_required
@render_to('players/pocket_detail.html')
def pocket_detail(request):
    """
    Show me what's in your pocketsses
    """
    player = request.user.get_profile()
    items = []
    pocket = player.pocket_set.get()
    if pocket.has_phone:
        items.append(dict(name="Phone", qty=1))
    if pocket.has_camera:
        items.append(dict(name="Camera", qty=1))
    if pocket.has_compass:
        items.append(dict(name="Compass", qty=1))
    artifacts = player.pocketartifact_set.all()
    treasures = player.pockettreasure_set.all()
    for pocketitem in list(artifacts) + list(treasures):
        items.append(dict(name=pocketitem.item_name(), qty=pocketitem.qty,
                          flavour_text=pocketitem.item_desc))
    response = dict(items=items)
    # Do we need to inform the player of a pickpocketing incident?
    picks = Pickpocketing.objects.filter(victim=player,
                                         victim_informed=False)
    if picks.count() > 0:
        pick_messages = []
        for pick in picks:
            pick_messages.append(pick.inform)
            pick.victim_informed = True
            pick.save()
        response['message'] = pick_messages
    return HttpResponse(json.dumps(response))


@login_required
def pickpocket(request):
    """
    Make a pickpocketing attempt for a player
    """
    if not request.is_ajax():
        return HttpResponse("No")
    player = request.user.get_profile()
    place = Place.objects.get(pk=request.POST['place_id'])
    target = Player.objects.get(pk=request.POST['player_id'])
    message, result = pickpocketing(player, target, place)
    return HttpResponse(
        json.dumps({'msg': message,
                    'result': result}))
@login_required
def player_detail(request):
    """
    Return the player's details
    """
    if not request.is_ajax():
        return HttpResponse("No")
    player = Player.objects.get(pk=request.POST['player_id'])
    news = player.newsitem_set.all()
    if news.count() == 0:
        newsitems = False
    else:
        newsitems = []
        for item in news:
            newsitems.append(dict(message=item.message,
                                  icon=item.icon.url))
    places_visited = player.visit_set.all().count()

    return HttpResponse(json.dumps(dict(newsitems=newsitems,
                                        id=player.pk,
                                        name=player.__unicode__(),
                                        places_visited=places_visited)))
