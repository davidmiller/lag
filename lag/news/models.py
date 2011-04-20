from datetime import datetime

from django.db import models

class NewsType(models.Model):
    """
    Category for news items
    """
    def upload_news_icon(instance, filename):
        """
        Generate the path to the npc icon

        Arguments:
        - `instance`:
        - `filename`:
        """
        sane_name = filename.lower().replace(' ', '')
        return "newsicons/%s" % sane_name


    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to=upload_news_icon,
                             blank=True, null=True)

    def __unicode__( self ):
        return self.name


class NewsItem(models.Model):
    """
    A prospective entry in a Player's NewsFeed,
    registered by some interaction.
    """
    newstype = models.ForeignKey(NewsType)
    place = models.ForeignKey('locations.Place')
    player = models.ForeignKey('players.Player')
    treasure = models.ForeignKey('items.Treasure', blank=True, null=True)
    artifact = models.ForeignKey('items.Artifact', blank=True, null=True)
    message = models.TextField()
    datetime = models.DateTimeField(default=datetime.now)

    def __unicode__( self ):
        return self.message

def news_feed(player):
    """
    Return the NewsItem events that will make up this player's NewsFeed

    Arguments:
    - `player`: Player
    """
    newsitems = NewsItem.objects.exclude(
        player=player
        ).order_by('-datetime')[:6]
    return [(n.message, n.newstype.icon) for n in newsitems]
