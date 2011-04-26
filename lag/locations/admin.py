from django.contrib.gis import admin

from lag.locations.models import (Region, Place, Lair, Visit, PlaceType,
                                  WallNote)

class WallNoteInline(admin.StackedInline):
    "Add notes to places inline"
    model = WallNote
    extra = 0

class PlaceAdmin(admin.GeoModelAdmin):
    """
    Edit Places manually in the admin site.
    """
    list_display = ("name", "point", "placetype")
    search_fields = ["name",]
    list_filter = ["placetype"]
    inlines = (WallNoteInline,)

admin.site.register(Region)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Lair, admin.GeoModelAdmin)
admin.site.register(Visit)
admin.site.register(PlaceType)
admin.site.register(WallNote)
