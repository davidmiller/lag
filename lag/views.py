from django.http import HttpResponseRedirect

from lag.utils.shortcuts import render_to

@render_to('homepage.html')
def homepage(request):
    """
    The Homepage!

    Arguments:
    - `request`:
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    return {}

