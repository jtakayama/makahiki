import datetime

from django.db import models

from managers.team_mgr.models import Team

class PowerData(models.Model):
    team = models.ForeignKey(Team)
    current_power = models.IntegerField(default=0,)
    baseline_power = models.IntegerField(default=0,)

    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(editable=False, auto_now=True)
