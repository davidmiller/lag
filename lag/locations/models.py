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
    created = models.DateTimeField(default=datetime.now)

    objects = models.GeoManager()

    class Meta:
        abstract = True

class PlaceType(models.Model):
    """
    A category for places - whether it is a pub station etc
    """
    name = models.CharField(max_length=200)
    soothsayer_percentage = models.IntegerField(default=10)
    wizard_percentage = models.IntegerField(default=10)
    doctor_percentage = models.IntegerField(default=10)
    philosopher_percentage = models.IntegerField(default=10)
    epic_percentage = models.IntegerField(default=0)
    mythic_percentage = models.IntegerField(default=0)
    artifact_percentage = models.IntegerField(default=0)

    def __unicode__( self ):
        return self.name

class Place(Location):
    """
    A public place - Cafe Etc
    """
    placetype = models.ForeignKey(PlaceType, blank=True, null=True,
                                  default=None)
    visits = models.IntegerField(default=0)
    unique_visitors = models.IntegerField(default=0)
    items_found = models.IntegerField(default=0)
    created_by = models.ForeignKey('players.Player', null=True, blank=True)
    current_visitors = models.ManyToManyField('players.Player',
                                              related_name='current_visitors')
    pickpocketings = models.IntegerField(default=0)

    def __unicode__(self):
        if self.name:
            return self.name
        return "Place: %s %s" % (self.lat, self.lon)

    def current_json(self, player):
        """
        Return a json representation of the current players at this Place

        `player`: Player
        """
        current = self.current_visitors.exclude(id=player.pk)
        if current.count() == 0:
            return False
        return [{'name': p.__unicode__(), 'id': p.pk} for p in current]

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

class WallNote(models.Model):
    """
    Comments left on the walls of places
    """
    place = models.ForeignKey(Place)
    player = models.ForeignKey('players.Player')
    created = models.DateTimeField(default=datetime.now)
    note = models.TextField()

    def __unicode__( self ):
        return self.note[:15]
