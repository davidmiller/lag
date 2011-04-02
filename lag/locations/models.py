from datetime import date

from django.db import models


class Region(models.Model):
    """
    A larger container for MeatWorld places
    """
    name = models.CharField(max_length=200)
    lat = models.FloatField()
    lon = models.FloatField()

    def __unicode__( self ):
        return self.name

class Place(models.Model):
    """
    Ooh - look where we are now
    """
    name = models.CharField(max_length=200, null=True)
    lat = models.FloatField()
    lon = models.FloatField()
    region = models.ForeignKey(Region, null=True)
    created_by = models.ForeignKey('players.Player', null=True)

    def __unicode__(self):
        return self.name

class Checkin(models.Model):
    """
    Record how many times Player has visited Place
    """
    player = models.ForeignKey('players.Player')
    place = models.ForeignKey(Place)
    visits = models.IntegerField(default=0)
    last_visited = models.DateField(null=True, default=date.today)

    def __unicode__( self ):
        return "Checkin: %s at %s" % (self.player, self.place)
