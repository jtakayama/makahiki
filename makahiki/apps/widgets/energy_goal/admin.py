from django.contrib import admin

from widgets.energy_goal.models import TeamEnergyGoal

class TeamEnergyGoalAdmin(admin.ModelAdmin):
    list_display = ["team", ]
    readonly_fields = ("percent_reduction", "team")

admin.site.register(TeamEnergyGoal, TeamEnergyGoalAdmin)