from django.contrib.gis import admin

from lag.locations.models import Region, Place, Lair, Visit, PlaceType

class PlaceAdmin(admin.GeoModelAdmin):
    """
    Edit Places manually in the admin site.
    """
    list_display = ("name", "point", "placetype")
    search_fields = ["name",]
    list_filter = ["placetype"]

admin.site.register(Region)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Lair, admin.GeoModelAdmin)
admin.site.register(Visit)
admin.site.register(PlaceType)
