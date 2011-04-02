from django.contrib import admin

from lag.locations.models import Region, Place, Checkin

admin.site.register(Region)
admin.site.register(Place)
admin.site.register(Checkin)
