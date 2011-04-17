import os
from datetime import date
import json
import random

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from lag.locations.models import Place, Visit
from lag.npcs.models import SoothSayer, Wizard, Doctor, Philosopher
from lag.utils.shortcuts import render_to

@render_to('locations/place_detail.html')
def place_detail(request, id):
    """
    Show the detail for a particular place

    Arguments:
    - `id`:
    """
    place = get_object_or_404(Place, id=id)
    nearby = Place.objects.distance(place.point,
                                    field_name='point').order_by('distance')
    return dict(place=place, nearby=nearby[1:3])


@login_required
def checkin(request):
    """
    Check to see if place exists, if not, create it unnamed

    Then make checkin
    """
    if not request.is_ajax():
        return HttpResponse('No')
    player = request.user.get_profile()
    lat = request.POST['lat']
    lon = request.POST['lon']
    point = Point(x=float(lon), y=float(lat))

    places = Place.objects.distance(point).order_by('distance')[:5]
    try:
        guess = [places[0].pk, places[0].name]
    except IndexError:
        guess = False
    alternatives = []
    for place in places[1:]:
        alternatives.append([place.pk, place.name])
    return HttpResponse(json.dumps(dict(guess=guess,
                                        alternatives=alternatives)))

@login_required
def register_place(request):
    """
    We're going to be registering a new place from user energy
    """
    if not request.is_ajax():
        return HttpResponse('No')
    player = request.user.get_profile()
    name = request.POST['name']
    lat = request.POST['lat']
    lon = request.POST['lon']
    point = Point(x=float(lon), y=float(lat))
    place = Place(lat=lat, lon=lon, point=point, name=name, created_by=player)
    place.save()
    visit = Visit.objects.get_or_create(player=player, place=place)[0]
    visit.last_visited = date.today()
    visit.visits += 1
    visit.save()
    params = dict(
        name=name,
        created_by="You, just now!",
        player_visit_count=visit.visits
        )
    return HttpResponse(json.dumps(params))

    return HttpResponse()

@login_required
def visit(request):
    """
    The player has confirmed that they're visiting this place.

    Let's give them the relevant stats about it.
    """
    if not request.is_ajax():
        return HttpResponse('No')
    player = request.user.get_profile()
    place_id = request.POST['place_id']
    place = get_object_or_404(Place, pk=place_id)
    visit = Visit.objects.get_or_create(player=player, place=place)[0]
    if visit.visits == 0:
        place.unique_visitors += 1
    visit.last_visited = date.today()
    visit.visits += 1
    visit.save()
    place_visits = place.visit_set.all().count()
    place.visits += 1
    place.save()
    stats = dict(
        name=place.name,
        place_created=place.created.strftime("%Y-%m-%d"),
        visits=place.visits,
        unique_visitors=place.unique_visitors,
        items_found=place.items_found,
        player_visits=visit.visits
        )
    chanced = []
    npc_percs = (
        (SoothSayer, place.placetype.soothsayer_percentage),
        (Philosopher, place.placetype.philosopher_percentage),
        (Doctor, place.placetype.doctor_percentage),
        (Wizard, place.placetype.wizard_percentage),
        )
    for npc, percentage in npc_percs:
        if random.randrange(0, 101) < percentage:
            chanced.append(npc.objects.get(pk=1))

    npcs = []
    for npc in chanced:
        icon = npc.icon.url if npc.icon else False
        npc_dict = {
            "name": npc._meta.object_name,
            "description": npc.description,
            "icon": icon
            }
        interaction_count = npc.interactions.all().count()
        interaction_index = random.randrange(0, interaction_count)
        npc_dict['text'] = npc.interactions.all()[interaction_index].text
        npcs.append(npc_dict)
    return HttpResponse(json.dumps(dict(stats=stats, npcs=npcs)))

def logger(request):
    """
    Shall we just serialise everything to a file?
    """
    with open(os.path.join(settings.ROOT, 'post.log'), 'a') as logfile:
        logfile.write(json.dumps(request.POST)+"\n")
    return HttpResponse('Yes')
