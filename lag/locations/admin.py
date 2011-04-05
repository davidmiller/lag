from django.contrib.gis import admin

from lag.locations.models import Region, Place, Visit

admin.site.register(Region)
admin.site.register(Place, admin.GeoModelAdmin)
admin.site.register(Visit)
