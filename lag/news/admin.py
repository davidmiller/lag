from django.contrib import admin

from lag.news.models import NewsType, NewsItem

admin.site.register(NewsType)
admin.site.register(NewsItem)
