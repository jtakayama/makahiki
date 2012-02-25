from django.contrib import admin

from widgets.energy_goal.models import TeamEnergyGoal

class TeamEnergyGoalAdmin(admin.ModelAdmin):
    list_display = ["team", "actual_usage", "goal_usage", "warning_usage", "updated_at"]

admin.site.register(TeamEnergyGoal, TeamEnergyGoalAdmin)