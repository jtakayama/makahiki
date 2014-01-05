"""heatmap visualization."""

from apps.managers.team_mgr.models import Group


def supply(request, page_name):
    """ Handle the request for viz_heatmap widget."""

    _ = page_name
    _ = request

    all_groups = Group.objects.order_by('name').all()

    for group in all_groups:
        group.teams = group.team_set.order_by('-name').all()
        for team in group.teams:
            wattdepot_source_name = team.energygoalsetting_set.all()[0].wattdepot_source_name
            if not wattdepot_source_name:
                wattdepot_source_name = team.name
            team.wattdepot_source_name = wattdepot_source_name

    return  {
        "all_groups": all_groups,
        }
