"""Provides the view of the widget."""
from apps.managers.team_mgr.models import Team,Group

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

def team_exists(team_name):
    """ Check if a Team exists with the same name as team_name. """
    result = False
    matches = Team.objects.filter(name=team_name)
    if len(matches) > 0:
        result = True
    return result
    
def create_new_team(team_name,group_name):
    """ Create a new Team object in the database. 
        team_name: A string with the name of the new Team.
        group_name: A string with the name of the group to assign the Team to. """
    result = False
    group_for_team = None
    
    # Retrieve the group that will be assigned to the new team
    group_check = Group.objects.all()
    for current_group in group_check:
        if current_group.name == group_name:
            group_for_team = current_group
            break
    if group_for_team is None:
        result = False
    else:
        # Create new Team
        new_team = Team()
        new_team.group = group_for_team
        new_team.name = team_name
        new_team.size = 0
        new_team.save()
        result = True
    return result

def group_exists(group_name):
    """ Check if a Group exists with the same name as group_name. """
    result = False
    matches = Group.objects.filter(name=group_name)
    if len(matches) > 0:
        result = True
    return result

def supply(request, page_name):
    """ supply view_objects for widget rendering."""
    _ = request
    _ = page_name
    
    # Initialize variables
    new_team_result = None
    new_group_result = None
    teams_groups_changed = []
    
    # Handle POST request
    if request.method == 'POST':
        
        # Add a new team
        new_team_name = None
        assigned_group = None
        new_team_field_text = request.POST.getlist("new_team")
        if new_team_field_text != None and new_team_field_text != []:
            new_team_name = str(new_team_field_text[0]).strip()
            assigned_group = str(request.POST.getlist("assign_to_group")[0]).strip()
            # Ignore a blank input field
            if new_team_name != None and new_team_name != "":
                if len(new_team_name) > 50:
                    new_team_result = "Invalid team name: \"%s\": name is longer than 50 characters." % new_team_name
                elif team_exists(new_team_name):
                    new_team_result = "Invalid team name \"%s\": name is already in use." % new_team_name
                else:
                    create_new_team_result = create_new_team(new_team_name,assigned_group)
                    if not create_new_team_result:
                        new_team_result = "Failed to create team \"%s.\"" % new_team_name
                    else:
                        new_team_result = "Team \"%s\" was created." % new_team_name
        else:
            new_team_result = None
        # End of code to add a new team
        
        # Add a new group
        new_group_name = None
        new_group_field_text = request.POST.getlist("new_group")
        if new_group_field_text != None and new_group_field_text != []:
            new_group_name = str(new_group_field_text[0]).strip()
            if new_group_name != None and new_group_name != "":
                if len(new_group_name) > 200:
                    new_group_result = "Invalid group name: \"%s\": name is longer than 200 characters." % new_group_name
                elif group_exists(new_group_name):
                    new_group_result = "Invalid group name \"%s\": name is already in use." % new_group_name
                else:
                    new_group = Group()
                    new_group.name = new_group_name
                    new_group.save()
                    new_group_result = "Group \"%s\" was created." % new_group_name
        else:
            new_group_result = None
        # End of code to add a new group
        
        # Change team groups
        teams_to_change = request.POST.getlist("change_team_group[]")
        team_set_groups = request.POST.getlist("set_group[]")
        if teams_to_change != []:
            team_set_groups_parsed = []
            for entry in team_set_groups:
                # The string passed in from the index.html select input is comma-separated: "team,group"
                entry_parsed = entry.split(",")
                team_set_groups_parsed.append(entry_parsed)
            for entry2 in team_set_groups_parsed:
                # Expected order: [team,group]
                if entry2[0] in teams_to_change:
                    entry2_matches = Team.objects.filter(name=entry2[0])
                    if len(entry2_matches) == 1:
                        group_matches = Group.objects.filter(name=entry2[1])
                        if len(group_matches) == 1:
                            entry2_matches[0].group = group_matches[0]
                            entry2_matches[0].save()
                            teams_groups_changed.append("Team \"%s\" changed to group \"%s\"." % (entry2[0],entry2[1]))
                        elif len(group_matches) > 1:
                            teams_groups_changed.append("Could not change team \"%s\" to group \"%s\": multiple groups matched this name." % (entry2[0], entry2[1]))
                    elif len(entry2_matches) > 1:
                        teams_groups_changed.append("Could not change team \"%s\" to group \"%s\": multiple teams matched this name." % (entry2[0], entry2[1]))
                    elif len(entry2_matches) == 0:
                        # A team that is deleted in the delete_teams_and_groups widget is still temporarily displayed in this widget.
                        # The deleted team is no longer displayed after this widget's "Save" button is clicked again.
                        # If the user attempted to modify the deleted team, this message will appear.
                        teams_groups_changed.append("Team \"%s\" in group \"%s\" does not exist." % (entry2[0], entry2[1]))
        else:
            teams_groups_changed = None    
        # End of code to change team groups
    
    # Set the new list of teams and groups after carrying out any changes.
    groups = Group.objects.all()
    teams_and_groups = get_teams()
            
    return{
        "new_team_result": new_team_result,
        "new_group_result": new_group_result,
        "groups": groups,
        "teams_groups_changed": teams_groups_changed,
        "teams_and_groups": teams_and_groups
    }
