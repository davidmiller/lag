"""
Main player models
"""
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db import models

from lag.registration.backends.default import (DefaultBackend as
                                           RegistrationBackend)
from lag.registration.signals import user_activated

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
    lair = models.ForeignKey('locations.Place', null=True, blank=True,
                             default=None)

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
    login(request, user)
    return player

user_activated.connect(create_player, sender=RegistrationBackend)
