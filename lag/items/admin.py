from django.contrib import admin

from lag.items.models import Artifact, Treasure, YNAcquisition

class YNInline(admin.StackedInline):
    """
    Create Acquisition models on the same admin page
    """
    model = YNAcquisition
    max_num = 1


class ItemAdmin(admin.ModelAdmin):
    """
    Interface for editing Items
    """
    inlines = [YNInline]


admin.site.register(Artifact, ItemAdmin)
admin.site.register(Treasure, ItemAdmin)
