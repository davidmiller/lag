import random

OPTIONS = ['ROCK', 'PAPER', 'SCISSORS']

def roshambo():
    """
    Return a list of a NPC's turns in roshambo
    """
    return [OPTIONS[random.randrange()] for x in xrange(0, 3)]
