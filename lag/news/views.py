import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from lag.news.models import news_feed

@login_required
def newsfeed(request):
    """
    JSON representation of a player's NewsFeed
    """
    player = request.user.get_profile
    newsfeed = news_feed(player)
    return HttpResponse(json.dumps(newsfeed))
