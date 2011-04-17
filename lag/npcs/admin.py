from django.contrib import admin

from lag.npcs.models import (NPCInteraction, SoothSayer, Wizard, Doctor,
                             Philosopher)
class NPCAdmin(admin.ModelAdmin):
    """
    Let's display the interactions slightly nicer
    """
    filter_horizontal = ['interactions']

admin.site.register(SoothSayer, NPCAdmin)
admin.site.register(Wizard, NPCAdmin)
admin.site.register(Doctor, NPCAdmin)
admin.site.register(Philosopher, NPCAdmin)
admin.site.register(NPCInteraction)
