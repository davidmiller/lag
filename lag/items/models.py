"""
Database representations of in-game-objects
"""

from datetime import date

from django.db import models

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
