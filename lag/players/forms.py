from django.forms import ModelForm

from lag.players.models import Player

class PlayerForm(ModelForm):
    """
    Change Yerself
    """

    class Meta:
        model = Player
