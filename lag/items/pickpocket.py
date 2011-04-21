"""
Functions to determine the success of a pickpocketing
"""

import random

from lag.items.models import Pickpocketing

def get_items(player):
    """
    Return a list of all items of any type for player

    Arguments:
    - `Player`: Player
    """
    artifacts = player.pocketartifact_set.all()
    treasures = player.pockettreasure_set.all()
    return list(artifacts) + list(treasures)

def pickpocket_success(player, target, item, place):
    """
    `player` has successfully pickpocketed `target`

    This means that we must:
    * Create a Pickpocketing
    * move the item
    * update the place's stats
    * update the player's stats

    Arguments:
    - `player`: Player
    - `target`: Player
    - `item`: PocketItem
    - `place`: Place
    """
    pick = Pickpocketing(pickpocketer=player, victim=target,
                         place=place)
    pick.extract_from_pocketitem(item)
    pick.save()
    item.move_to(player)
    place.pickpocketings += 1
    place.save()
    player.pickpocketings += 1
    player.save()
    return pick

def pickpocket_failure(player, target, item, place):
    """
    If our pickpocketing attempt has failed, we must:

    * Kick the player out of the place

    Arguments:
    - `player`: Player
    - `target`: Player
    - `item`: PocketItem
    - `place`: Place
    """
    place.current_visitors.remove(player)

def pickpocketing(player, target, place):
    """
    See if player can pickpocket the target

    Arguments:
    - `player`: Player
    - `target`: Player
    - `place`: Place
    """
    itemlist = get_items(player)
    if len(itemlist) == 0:
        return ("! %s didn't have anything in their pocket" % target, True)
    item = itemlist[random.randrange(0, len(itemlist))]
    if random.randrange(0, 101) > 50:
        pick = pickpocket_success(player, target, item, place)
        msg =  "Congratulations! You swiped a %s from %s" % (
            item.item_name(),
            target)
        return (msg, True)
    else:
        pickpocket_failure(player, target, item, place)
        msg = "%s catches you trying to steal and kicks you out of %s"
        return (msg % (target, place), False)
