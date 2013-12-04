"""Handle rendering of the Energy Power Meter widget."""
from apps.widgets.resource_goal import resource_goal


def supply(request, page_name):
    """Return the view_objects content, which in this case is empty."""

    _ = page_name

    team = request.user.profile.team
    if team:
        goal = resource_goal.team_goal_settings(team, "energy")
        interval = goal.realtime_meter_interval
        wattdepot_source_name = goal.wattdepot_source_name
        if not wattdepot_source_name:
            wattdepot_source_name = team.name
    else:
        interval = None
        wattdepot_source_name = None
    width = 300
    height = 100
    return {"interval": interval,
            "wattdepot_source_name": wattdepot_source_name,
            "width": width,
            "height": height
            }
