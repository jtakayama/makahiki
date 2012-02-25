from django.contrib import admin

from widgets.energy_power_meter.models import PowerData

class PowerDataAdmin(admin.ModelAdmin):
    list_display = ["team", "current_power", "baseline_power"]

admin.site.register(PowerData, PowerDataAdmin)