"""Provides the view of the widget."""
from apps.managers.team_mgr.models import Team

def get_teams():
    """ Returns a list of [team,group] lists. """
    team_list = Team.objects.all()
    teams_and_groups = []
    
    if team_list is None:
        teams_and_groups.append(["No teams","No groups"])
    else:
        for current_team in team_list:
            if current_team.group != None:
                teams_and_groups.append([current_team.name,current_team.group])
            else:
                teams_and_groups.append([current_team.name, "None"])
    
    return teams_and_groups

def supply(request, page_name):
    """ supply view_objects for widget rendering."""
    _ = request
    _ = page_name
    
    teams_deleted = []
    
    # Delete teams
    teams_to_delete = request.POST.getlist("delete_team[]")
    if len(teams_to_delete) > 0:
        for team_name in teams_to_delete:
            matches = Team.objects.filter(name=team_name)
            if len(matches) == 1:
                matches[0].delete()
                teams_deleted.append("Team \"%s\" was deleted." % team_name)
            else:
                teams_deleted.append("Could not delete team \"%s\" : multiple teams matched this name." % team_name)
        else:
            teams_deleted = None
    # End of code to delete teams
    
    # Set the new list of teams after carrying out any creations or deletions.
    teams_and_groups = get_teams()    
    
    return {
        "teams_deleted": teams_deleted,
        "teams_and_groups": teams_and_groups
    }
