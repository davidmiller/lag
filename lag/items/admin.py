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
    list_display = ['name', 'released', 'quantity']
    list_filter = ['released']

class TreasureAdmin(ItemAdmin):
    """
    Treasure specific interfaces
    """
    list_display = ['name', 'category', 'released', 'quantity']
    list_filter = ['category', 'released']


admin.site.register(Artifact, ItemAdmin)
admin.site.register(Treasure, TreasureAdmin)
