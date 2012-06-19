"""badge model."""
from django.db import models
from datetime import datetime
from django.conf import settings
from apps.managers.player_mgr.models import Profile
from apps.utils.utils import media_file_path


_MEDIA_LOCATION = "badges"
"""location for uploaded files."""


class Badge(models.Model):
    """Defines Badge model."""
    THEME_CHOICES = (
                     ('1', "theme 1"),
                     ('2', "theme 2"),
                     ('3', "theme 3"),
                     ('4', "theme 4"),
                     ('5', "theme 5"),
                     )

    name = models.CharField(max_length=255,
                            help_text="The name of the badge")
    label = models.CharField(max_length=20,
                            help_text="The label of the badge")
    description = models.CharField(max_length=255,
                                   help_text="The description of the badge")
    hint = models.CharField(max_length=255,
                            help_text="The Hint of the badge")
    slug = models.CharField(max_length=255,
                            help_text="Automatically generated if left blank.")
    image = models.ImageField(
        max_length=255, blank=True, null=True,
        upload_to=media_file_path(_MEDIA_LOCATION),
        help_text="The image of the badge.",)
    award_condition = models.CharField(
        max_length=1024,
        help_text="if the condition is True, the badge will be awarded. " +
                   settings.PREDICATE_DOC_TEXT)
    theme = models.CharField(max_length=1, choices=THEME_CHOICES, default='6',
                             help_text="The theme for the badge.")

    def __unicode__(self):
        return self.name


class BadgeAward(models.Model):
    """Defines model for awarded badge."""
    profile = models.ForeignKey(Profile)
    badge = models.ForeignKey(Badge)
    awarded_at = models.DateTimeField(default=datetime.now)
