from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from lag.players.forms import PlayerForm
from lag.utils.shortcuts import render_to

@render_to('players/home.html')
def home(request):
    """
    Let's see what we do with this user...

    Arguments:
    - `req`:
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    player = request.user.get_profile()
    return dict(player=player)

@login_required
@render_to('players/edit_profile.html')
def edit_profile(request):
    """
    Change yer profile

    Arguments:
    - `request`: HttpRequest
    """
    player = request.user.get_profile()
    if request.method == 'POST':
        form = PlayerForm(request.POST, request.FILES, instance=player)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/home/')
    else:
        form = PlayerForm(instance=player)
    return dict(form=form, player=player)
