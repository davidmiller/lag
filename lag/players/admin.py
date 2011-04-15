from django.contrib import admin

from lag.players.models import Player, Pocket, PocketArtifact, PocketTreasure

class PocketInline(admin.StackedInline):
    """
    Display the player's pocket in their admin page
    """
    model = Pocket
    extra = 0

class PocketTreasureInline(admin.StackedInline):
    """
    Display the player's Treasures in their admin page
    """
    model = PocketTreasure
    extra = 0

class PocketArtifactInline(admin.StackedInline):
    """
    Display the player's Artifacts in their admin page
    """
    model = PocketArtifact
    extra = 0


class PlayerAdmin(admin.ModelAdmin):
    """
    Can we have a nice administrative interface for players
    """
    inlines = [PocketInline, PocketTreasureInline, PocketArtifactInline]


admin.site.register(Player, PlayerAdmin)
admin.site.register(Pocket)
admin.site.register(PocketArtifact)
admin.site.register(PocketTreasure)
