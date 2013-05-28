'''Holds the Models for the Smartgrid_mgr.
Created on May 24, 2013

@author: Cam Moore
'''
from django.db import models
from django.contrib.auth.models import User


class GccSettings(models.Model):
    """Represents the individual user's choices for running different Grid Consistency Checker
    checks."""
    user = models.ForeignKey(User)
    check_pub_dates = models.BooleanField(default=True,
                                          help_text="Run the check publication and " + \
                                          "expiration date checks.")
    check_event_dates = models.BooleanField(default=True,
                                            help_text="Run check event dates.")
    check_unlock_dates = models.BooleanField(default=True,
                                             help_text="Run check unlock condition dates.")
    check_unreachable = models.BooleanField(default=True,
                                            help_text="Run check unreachable actions.")
    check_false_unlocks = models.BooleanField(default=True,
                                              help_text="Run check false unlock conditions.")
    check_mismatched_levels = models.BooleanField(default=True,
                                                  help_text="Run mismatched level check.")
    check_description_urls = models.BooleanField(default=False,
                                                 help_text="Run check description URLs, very slow.")
