from django.contrib.gis import admin

from lag.locations.models import Region, Place, Lair, Visit, PlaceType

admin.site.register(Region)
admin.site.register(Place, admin.GeoModelAdmin)
admin.site.register(Lair, admin.GeoModelAdmin)
admin.site.register(Visit)
admin.site.register(PlaceType)
