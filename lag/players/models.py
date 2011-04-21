"""
Main player models
"""
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db import models

from registration.backends.default import (DefaultBackend as
                                           RegistrationBackend)
from registration.signals import user_activated


class Player(models.Model):
    """
    Someone playing our game!
    """
    def upload_profile_pic(instance, filename):
        """
        Generate the path to the profile picture

        Arguments:
        - `instance`:
        - `filename`:
        """
        sane_name = filename.lower().replace(' ', '')
        username = instance.user.username
        return "profiles/%s/%s" % (username, sane_name)

    user = models.ForeignKey(User)
    firstname = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    short_bio = models.CharField(max_length=400, blank=True, null=True)
    profile_pic = models.ImageField(upload_to=upload_profile_pic,
                                    blank=True, null=True)
    lairs = models.ManyToManyField('locations.Lair', null=True, blank=True,
                             default=None)
    has_lair = models.BooleanField(default=False)
    interactions_seen = models.ManyToManyField('npcs.NPCInteraction')
    pickpocketings = models.IntegerField(default=0)

    def __unicode__( self ):
        if self.surname and self.firstname:
            return "%s %s" % (self.firstname, self.surname)
        return self.user.username

def create_player(sender, user, request, **kwargs):
    """
    Generate an Player for new users on activation

    Arguments:
    - `sender`:
    - `instance`:
    - `creted`:
    - `**kwargs`:
    """
    player = Player(user=user)
    player.save()
    pocket = Pocket(player=player)
    pocket.save()
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return player

user_activated.connect(create_player, sender=RegistrationBackend)


class Pocket(models.Model):
    """
    A player has a pocket, in which they keep any number of increasingly
    unlikely Artifacts.
    """
    player = models.ForeignKey(Player, unique=True)
    has_phone = models.BooleanField(default=False)
    has_camera = models.BooleanField(default=False)
    has_compass = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s's Pocket" % self.player.__unicode__()


class PocketItem(models.Model):
    """
    A player stores various Items in various quantities in their Pocket.
    """
    player = models.ForeignKey(Player, blank=True, null=True)
    qty = models.IntegerField(default=0)

    class Meta:
        abstract = True

    def _move_to(self, stolen):
        """
        ABC portion of the move functionality

        Arguments:
        - `stolen`: PocketItem
        """
        stolen.qty += 1
        stolen.save()

        self.qty -= 1
        if self.qty == 0:
            self.delete()
        else:
            self.save()


class PocketArtifact(PocketItem):
    """
    Artifacts in the pocket
    """
    artifact = models.ForeignKey('items.Artifact')

    def __unicode__( self ):
        return "PocketArtifact: %s x %s" % (self.artifact, self.qty)

    def move_to(self, target):
        """
        Move one of ourself to `target`

        Arguments:
        - `target`: Player
        """
        stolen = PocketArtifact.objects.get_or_create(
            player=target, artifact=self.artifact)[0]
        self._move_to(stolen)

    def item_name(self):
        "Return the artifact desc"
        return self.artifact.name


class PocketTreasure(PocketItem):
    """
    Treasures in the pocket
    """
    treasure = models.ForeignKey('items.Treasure')

    def __unicode__( self ):
        return "PocketTreasure: %s x %s" % (self.treasure, self.qty)

    def move_to(self, target):
        """
        Move one of ourself to `target`

        Arguments:
        - `target`: Player
        """
        stolen = PocketTreasure.objects.get_or_create(
            player=target, treasure=self.treasure)[0]
        self._move_to(stolen)

    def item_name(self):
        "Return the treasure desc"
        return self.treasure.name
