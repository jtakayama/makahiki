import datetime

from django.db import models
from django.contrib.auth.models import User

from managers.team_mgr.models import Team

# Create your models here.

class TeamEnergyGoal(models.Model):
    # The amount of points to award for completing a goal.
    GOAL_POINTS = 20

    team = models.ForeignKey(Team)
    percent_reduction = models.IntegerField(default=0, editable=False)
    goal_usage = models.DecimalField(decimal_places=2, max_digits=10, editable=False)
    actual_usage = models.DecimalField(decimal_places=2, max_digits=10, editable=False)

    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(editable=False, auto_now=True)

    def save(self, *args, **kwargs):
        """Overrided save method to award the goal's points to members of the team."""
        goal_completed = self.goal_usage and self.actual_usage and (
        self.actual_usage <= self.goal_usage)
        super(TeamEnergyGoal, self).save(*args, **kwargs)

        if self.team and goal_completed:
            count = 0
            # Award points to the members of the team.
            for profile in self.team.profile_set.all():
                if profile.setup_complete:
                    today = datetime.datetime.today()
                    # Hack to get around executing this script at midnight.  We want to award
                    # points earlier to ensure they are within the round they were completed.
                    if today.hour == 0:
                        today = today - datetime.timedelta(hours=1)

                    date = "%d/%d/%d" % (today.month, today.day, today.year)
                    profile.add_points(self.GOAL_POINTS, today, "Team Energy Goal for %s" % date,
                        self)
                    profile.save()
                    count = count + 1
            print '     %s users in the lounge awarded %s points each' % (count, self.GOAL_POINTS)
          
      
    
