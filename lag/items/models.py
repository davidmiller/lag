"""
Database representations of in-game-objects
"""

from datetime import date, datetime

from django.db import models

from lag.utils.functions import qs_rand

class Item(models.Model):
    """
    Abstract base class for Items.

    Contains Metadata suitable for all In-Game-Objects
    """
    name = models.CharField(max_length=200)
    released = models.BooleanField(default=False)
    created_date = models.DateField(default=date.today)
    released_date = models.DateField(blank=True, null=True)
    flavour_text = models.TextField(null=True)

    class Meta:
        abstract = True


class Artifact(Item):
    """
    In-Game Artifacts - these are Collectable but not exceedingly rare Items
    """
    quantity = models.IntegerField(default=0)

    def __unicode__( self ):
        return self.name

    @staticmethod
    def rand_artifact():
        """
        Return a random Artifact
        """
        return qs_rand(Artifact.objects.all())


class Treasure(Item):
    """
    Treasures are rare, highly prized items.

    They fall into two categories - Epic & Mythic
    """
    CAT_CHOICES = (
        ("EPIC", "Epic"),
        ("MYTHIC", "Mythic"),
        )

    category = models.CharField(max_length=10, choices=CAT_CHOICES)
    quantity = models.IntegerField(default=0)

    def __unicode__( self ):
        return self.name

    @staticmethod
    def rand_epic():
        """
        Return a random Epic Treasure
        """
        return qs_rand(Treasure.objects.filter(category="EPIC"))

    @staticmethod
    def rand_mythic():
        """
        Return a random Mythin Treasure
        """
        return qs_rand(Treasure.objects.filter(category="MYTHIC"))


class YNAcquisition(models.Model):
    """
    An acquisition for an item based on Text, Yes/No, with responses for both.
    """
    artifact = models.ForeignKey(Artifact, blank=True, null=True)
    treasure = models.ForeignKey(Treasure, blank=True, null=True)
    dilemma = models.TextField()
    yes = models.TextField()
    no = models.TextField()

    def __unicode__( self ):
        return self.dilemma[:12]

class Pickpocketing(models.Model):
    """
    A pickpocketing that has occurred
    """
    pickpocketer = models.ForeignKey('players.Player')
    victim = models.ForeignKey('players.Player', related_name="victim")
    place = models.ForeignKey('locations.Place')
    occurred = models.DateTimeField(default=datetime.now)
    victim_informed = models.BooleanField(default=False)
    artifact = models.ForeignKey(Artifact, blank=True, null=True)
    treasure = models.ForeignKey(Treasure, blank=True, null=True)

    def __unicode__( self ):
        return "A pickpocketing!"

    def extract_from_pocketitem(self, item):
        """
        Figure out what kind of item we're pickpocketing and
        assign it to the relevant field

        Arguments:
        - `item`: PocketItem
        """
        from lag.players.models import PocketArtifact, PocketTreasure
        if isinstance(item, PocketArtifact):
            self.artifact = item.artifact
        elif isinstance(item, PocketTreasure):
            self.treasure = item.treasure
        else:
            raise ValueError

    def get_item_name(self):
        """
        Gloss over the multiple Item models
        """
        if self.artifact:
            return self.artifact.name
        return self.treasure.name

    @property
    def inform(self):
        """
        The message that will be passed back to the client when we inform
        someone that they've been pickpocketed
        """
        msg_tpl = "Cripes - It looks like you've been pickpocketed! %s is missing from your pocket!... "
        return msg_tpl % self.get_item_name()


