"""
Background callback tasks for time-related location activity
"""

from celery.decorators import task

@task
def end_visit(place_id, player_id):
    """
    Remove the player from the list of current visitors to this place
    """
    from lag.players.models import Player
    from lag.locations.models import Place

    player = Player.objects.get(pk=player_id)
    place = Place.objects.get(pk=place_id)
    place.current_visitors.remove(player)
    return True
