"""
 provides competition settings in the request context to be used within
 a template. It mainly retrieve the settings from settings files.
"""
from django.conf import settings
from apps.managers.settings_mgr import get_current_round_info, in_competition
from apps.managers.player_mgr.models import Profile
from apps.managers.team_mgr.models import Team


def competition(request):
    """Provides access to standard competition constants within a template."""
    # Get user-specific information.

    user = request.user
    team_member_count = None
    if user.is_authenticated() and user.get_profile().team:
        team_member_count = user.get_profile().team.profile_set.count()

    team_count = Team.objects.count()
    overall_member_count = Profile.objects.count()

    # Get Facebook info.
    try:
        facebook_app_id = settings.FACEBOOK_APP_ID
    except AttributeError:
        facebook_app_id = None

    return {
        "STATIC_URL": settings.STATIC_URL,
        "SITE_NAME": settings.CHALLENGE.site_name,
        "COMPETITION_NAME": settings.CHALLENGE.competition_name,
        "COMPETITION_POINT_LABEL": settings.CHALLENGE.competition_point_label,
        "CSS_THEME": settings.CHALLENGE.theme,
        "THEME_NAME": settings.CHALLENGE.theme,
        "TEAM_COUNT": team_count,
        "TEAM_MEMBER_COUNT": team_member_count,
        "OVERALL_MEMBER_COUNT": overall_member_count,
        "TEAM_LABEL": settings.CHALLENGE.competition_team_label,
        "CURRENT_ROUND_INFO": get_current_round_info(),
        "FACEBOOK_APP_ID": facebook_app_id,
        "IN_COMPETITION": in_competition(),
    }