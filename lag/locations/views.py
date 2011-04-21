"""
Views for location.

Provide the XHR/JSON API for location-related LAG interactions.
"""
import os
from datetime import date, datetime, timedelta
import json
import random

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from lag.locations.models import Place, Visit, PlaceType
from lag.locations.tasks import end_visit
from lag.items.models import Treasure, Artifact
from lag.news.models import NewsItem, NewsType
from lag.npcs.models import SoothSayer, Wizard, Doctor, Philosopher
from lag.players.models import PocketArtifact, PocketTreasure
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
    try:
        acc = int(request.POST['acc'])
    except ValueError:
        acc = float(request.POST['acc'])
    point = Point(x=float(lon), y=float(lat))

    # If Accuracy is high, just list places very close,
    # Otherwise, list places by # player visits to places
    # in that area.
    if acc < 200:
        places = Place.objects.distance(point).order_by('distance')[:5]
        try:
            guess = [places[0].pk, places[0].name]
        except IndexError:
            guess = False
        alternatives = []
        for place in places[1:]:
            alternatives.append([place.pk, place.name])

    else:
        area = (point, Distance(m=acc))
        places = Place.objects.filter(point__distance_lte=area)[:5]
        def visitsort(x):
            try:
                return x.visit_set.get(player=player).visits
            except Visit.DoesNotExist:
                return 0
        s_places = sorted(places, key=visitsort)
        guess = [s_places[-1].pk, s_places[-1].name]
        alternatives = []
        s_places.reverse()
        for place in s_places:
            if place.pk != guess[0]:
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
    placetype = PlaceType.objects.get(pk=request.POST['placetype'])
    lat = request.POST['lat']
    lon = request.POST['lon']
    point = Point(x=float(lon), y=float(lat))
    place = Place(lat=lat, lon=lon, point=point, name=name,
                  placetype=placetype, created_by=player)
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
    place.current_visitors.add(player)
    place.save()
    placetype = place.placetype

    # Let's register a callback to end this visit in 15 min
    callback_time = datetime.now() + timedelta(minutes=15)
    end_visit.apply_async(args=[place_id, player.pk], eta=callback_time)

    # Let's make a NewsItem of this.
    newsvisit = NewsType.objects.get(name="Visit")
    newsitem = NewsItem(newstype=newsvisit, place=place, player=player,
                        message=visit.__unicode__())
    newsitem.save()

    # Place Stats
    stats = dict(
        id=place.pk,
        name=place.name,
        place_created=place.created.strftime("%Y-%m-%d"),
        visits=place.visits,
        unique_visitors=place.unique_visitors,
        items_found=place.items_found,
        player_visits=visit.visits,
        current_visitors=place.current_visitors.all().count()
        )
    # NPCs
    chanced = []
    npc_percs = (
        (SoothSayer, placetype.soothsayer_percentage),
        (Philosopher, placetype.philosopher_percentage),
        (Doctor, placetype.doctor_percentage),
        (Wizard, placetype.wizard_percentage),
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
    # Items
    item = False
    if random.randrange(0, 101) < placetype.epic_percentage:
        item = Treasure.rand_epic()
        itemtype = "Epic"
    if not item and random.randrange(0, 101) < placetype.mythic_percentage:
        item = Treasure.rand_mythic()
        itemtype = "Mythic"
    if not item and random.randrange(0, 101) < placetype.artifact_percentage:
        item = Artifact.rand_artifact()
        itemtype = "Artifact"
    if item:
        item_dict = {
            'name': item.name,
            'flavour_text': item.flavour_text,
        }
        acquisition = item.ynacquisition_set.get()
        item_dict['acquisition'] = {
            'dilemma': acquisition.dilemma,
            'choices': {
                "yes": acquisition.yes,
                "no": acquisition.no
                },
            'callback': {
                'url': '/locations/acquire-item/',
                'params':{
                    'item_id': item.id,
                    'itemtype': itemtype,
                    'place_id': place.id
                    }
                }
            }

    else:
        item_dict = item
    return HttpResponse(
        json.dumps(dict(stats=stats, npcs=npcs,
                        item=item_dict,
                        current_visitors=place.current_json()))
        )

@login_required
def acquire_item(request):
    """
    A player has successfully completed the acquisition model
    for an item that they found while visiting a place.
    """
    if not request.is_ajax():
        return HttpResponse('No')
    player = request.user.get_profile()
    itemtype = request.POST['itemtype']
    # Get the item and add it to the player's Pocket
    if itemtype == 'Artifact':
        item = Artifact.objects.get(pk=request.POST['item_id'])
        pocket_item = PocketArtifact.objects.get_or_create(player=player,
                                                           artifact=item)[0]
        pocket_item.qty += 1
        pocket_item.save()
    else:
        item = Treasure.objects.get(pk=request.POST['item_id'])
        pocket_item = PocketTreasure.objects.get_or_create(player=player,
                                                           treasure=item)[0]
        pocket_item.qty += 1
        pocket_item.save()
    # Increment the Place's items found count
    place = Place.objects.get(pk=request.POST['place_id'])
    place.items_found += 1
    place.save()
    # Add a news item for other players
    news_msg = "%s found %s at %s" % (player.__unicode__(),
                                      item.__unicode__(), place.__unicode__())
    acquisition = NewsType.objects.get(name="Acquisition")
    newsitem = NewsItem(newstype=acquisition, place=place, player=player,
                        message=news_msg)
    if itemtype == "Artifact":
        newsitem.artifact = item
    else:
        newsitem.Treasure = item
    newsitem.save()


    msg = "%s added to your pocket" % pocket_item.__unicode__()
    acquired_msg = {'message': msg}
    return HttpResponse(json.dumps(acquired_msg))

def logger(request):
    """
    Shall we just serialise everything to a file?
    """
    with open(os.path.join(settings.ROOT, 'post.log'), 'a') as logfile:
        logfile.write(json.dumps(request.POST)+"\n")
    return HttpResponse('Yes')
