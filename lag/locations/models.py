from datetime import date, datetime

from django.contrib.gis.db import models


class Region(models.Model):
    """
    A larger container for MeatWorld places
    """
    name = models.CharField(max_length=200)
    lat = models.FloatField()
    lon = models.FloatField()

    def __unicode__( self ):
        return self.name

class Location(models.Model):
    """
    Abstract class for Locations
    """
    name = models.CharField(max_length=200, null=True)
    lat = models.FloatField()
    lon = models.FloatField()
    region = models.ForeignKey(Region, null=True, blank=True)
    point = models.PointField(srid=4326)
    created = models.DateField(default=datetime.now)

    objects = models.GeoManager()

    class Meta:
        abstract = True

class Place(Location):
    """
    A public place - Cafe Etc
    """
    created_by = models.ForeignKey('players.Player', null=True, blank=True)

    def __unicode__(self):
        if self.name:
            return self.name
        return "Place: %s %s" % (self.lat, self.lon)

class Lair(Location):
    """
    A player has a lair.
    """
    created_by = models.ForeignKey('players.Player', null=True, blank=True,
                                   related_name="lair_createdby")
    active = models.BooleanField(default=True)

    def __unicode__( self ):
        return self.name


class Visit(models.Model):
    """
    Record how many times Player has visited Place
    """
    player = models.ForeignKey('players.Player')
    place = models.ForeignKey(Place)
    visits = models.IntegerField(default=0)
    last_visited = models.DateField(null=True, default=date.today)

    def __unicode__( self ):
        msg_tpl = "%s visited %s at %s for the %sth time"
        return msg_tpl % (self.player.__unicode__(), self.place.__unicode__(),
                          self.last_visited, self.visits)
