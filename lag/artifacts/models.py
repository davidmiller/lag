from django.db import models

class Artifact(models.Model):
    """
    In - Game Artifacts
    """
    name = models.CharField(max_length=200)

    def __unicode__( self ):
        return self.name

