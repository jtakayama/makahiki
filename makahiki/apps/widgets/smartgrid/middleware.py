"""
This middleware to reward points to completing the setup wizard.
It will create an approved activitymember.
"""

import datetime
from django.conf import settings
from widgets.badges import user_badges
from lib.brabeion import badges
from widgets.smartgrid.models import Activity, ActivityMember

class SetupCompleteMiddleware(object):
    """
    It will create an approved activitymember for the setup activity
    """

    def process_request(self, request):
        """Checks if the user is logged in."""
        user = request.user
        if user.is_authenticated():
            profile = request.user.get_profile()

            if profile.setup_complete == True:
                activity_name = settings.SETUP_WIZARD_ACTIVITY_NAME
                try:
                    activity = Activity.objects.get(name=activity_name)
                    member, _ = ActivityMember.objects.get_or_create(activity=activity, user=profile.user)
                    if member.approval_status != "approved":
                        member.approval_status="approved"
                        member.save()

                except Activity.DoesNotExist:
                    pass

        return None
