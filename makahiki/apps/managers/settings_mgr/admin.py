"""
settings manager Admin
"""
from django.contrib import admin
from apps.managers.settings_mgr.models import ChallengeSettings, RoundSettings

admin.site.register(ChallengeSettings)
admin.site.register(RoundSettings)