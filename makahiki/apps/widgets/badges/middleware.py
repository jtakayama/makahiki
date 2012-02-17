"""
This middleware awards possible badges to user.
"""

import datetime
from widgets.badges import user_badges
from lib.brabeion import badges

class AwardBadgeMiddleware(object):
    """
    This middleware awards possible badges to user.
    """

    def process_request(self, request):
        """Checks if the user is logged in."""
        user = request.user
        if user.is_authenticated():
            if user.badges_earned.filter(slug="dailyvisitor").count() == 0:
                badges.possibly_award_badge(
                    user_badges.DailyVisitorBadge.slug, user=request.user)

        return None
