from django.db import models

class NPCInteraction(models.Model):
    """
    The text that an NPC will 'say' to a player
    """
    text = models.TextField()
    level = models.IntegerField(default=0)

    def __unicode__( self ):
        return "NPC: %s" % self.text[:10]


class NPC(models.Model):
    """
    ABC for NPCs
    """
    def upload_npc_icon(instance, filename):
        """
        Generate the path to the npc icon

        Arguments:
        - `instance`:
        - `filename`:
        """
        sane_name = filename.lower().replace(' ', '')
        npc_name = instance._meta.object_name
        return "npcs/%s/%s" % (npc_name, sane_name)

    icon = models.ImageField(upload_to=upload_npc_icon, blank=True, null=True)
    description = models.TextField()
    interactions = models.ManyToManyField(NPCInteraction)

    class Meta:
        abstract = True


class SoothSayer(NPC):
    """
    A soothsayer Character.
    """

    def __unicode__( self ):
        return "SoothSayer"

class Wizard(NPC):
    """
    A wizard Character.
    """

    def __unicode__( self ):
        return "Wizard"

class Doctor(NPC):
    """
    A doctor Character.
    """

    def __unicode__( self ):
        return "Doctor"

class Philosopher(NPC):
    """
    A philosopher Character.
    """

    def __unicode__( self ):
        return "Philosopher"


