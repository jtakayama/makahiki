from django.contrib import admin

from widgets.energy_scoreboard.models import EnergyData

class EnergyDataAdmin(admin.ModelAdmin):
    list_display = ["team", "date", "energy",]

admin.site.register(EnergyData, EnergyDataAdmin)