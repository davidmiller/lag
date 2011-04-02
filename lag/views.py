from lag.utils.shortcuts import render_to

@render_to('homepage.html')
def homepage(request):
    """
    The Homepage!

    Arguments:
    - `request`:
    """
    return {}

