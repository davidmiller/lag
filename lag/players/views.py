"""
Let's get viewtastic with our players
"""

import json

from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from django.http import HttpResponseRedirect, HttpResponse

from lag.locations.models import Lair, Visit, PlaceType
from lag.players.forms import PlayerForm
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
    visits = Visit.objects.all().order_by('-last_visited')[:5]
    placetypes = PlaceType.objects.all()
    return dict(player=player, visits=visits, placetypes=placetypes)

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
    pocket = player.pocket_set.get()
    artifacts = player.pocketartifact_set.all()
    treasures = player.pockettreasure_set.all()

    return dict(player=player, pocket=pocket,
                artifacts=artifacts, treasures=treasures)
