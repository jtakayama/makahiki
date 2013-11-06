"""Provides the view of the widget."""
from apps.managers.team_mgr.models import Team

def get_teams():

    team_list = Team.objects.all()
    teams_and_groups = []
    
    if team_list is None:
        teams_and_groups.append(["No teams","No groups"])
    else:
        for current_team in team_list:
            teams_and_groups.append([current_team.name,current_team.group])
    
    return teams_and_groups

def supply(request, page_name):
    """ supply view_objects for widget rendering."""
    _ = request
    _ = page_name
    
    # Initialize empty variable
    teams_deleted = []
    
    # Handle POST request
    if request.method == 'POST':
        teams_to_delete = request.POST.getlist("delete_team[]")
        if len(teams_to_delete) > 0:
            for team_name in teams_to_delete:
                Team.objects.filter(name="%s" % team_name).delete()
                teams_deleted.append(team_name)
        else:
            teams_deleted = None
    
    # Set the new list of teams after carrying out any deletions
    teams_and_groups = get_teams()
            
    return{
        "teams_and_groups": teams_and_groups,
        "teams_deleted": teams_deleted
    }
