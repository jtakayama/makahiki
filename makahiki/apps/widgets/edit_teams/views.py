"""Provides the view of the widget."""
from apps.managers.team_mgr.models import Team,Group
#from django import forms
#from django.db import models

def get_teams():
    """ Retrieves a list of [team,group] lists. """
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
    """ Create a new Team object in the database. """
    result = False
    group_for_team = None
    
    # Retrieve the group that will be assigned to the new team
    group_check = Group.objects.all()
    for current_group in group_check:
        # Sanity checks related to a unicode bug
        print current_group.name  # This string from the database is not unicode
        print group_name # This user input from Django is unicode
        print current_group.name == group_name # This comparison always fails
        # end sanity checking code
        if current_group.name == group_name:
            group_for_team = current_group
            break
    print group_for_team
    if group_for_team is None:
        result = False
    else:
        print "Sanity check."
        # Create new Team
        new_team = Team()
        new_team.group = group_for_team
        new_team.name = team_name
        new_team.size = 0
        new_team.save()
        result = True
        
#     if len(group_check) == 1:
#         group_field = models.ForeignKey(Group,help_text="The group this team belongs to.")
#         group_field.clean(group_check[0])
#         
#         team_field = models.CharField(help_text="The team name", max_length=50)
#         team_field.clean(team_name)
#     
#         size_field = models.IntegerField()
#         size_field.clean(0)
#         
#         # Create new Team (does not work)
#         new_team = Team(group=group_field, team=team_field, size=size_field)
#         new_team.save()
#         # Check that team exists
#         if team_exists(team_name):
#             result = True
#         else:
#             result = False
#    else:
#        result = False
    return result

def supply(request, page_name):
    """ supply view_objects for widget rendering."""
    _ = request
    _ = page_name
    
    # Initialize variables
    groups = Group.objects.all()
    new_team_result = None
    teams_deleted = []
    
    # Handle POST request
    if request.method == 'POST':
        # Add a new team
        new_team_name = str(request.POST.getlist("new_team")[0]).strip()
        assigned_group = str(request.POST.getlist("assign_to_group")).strip()
        if new_team_name != None:
            if len(new_team_name) > 50:
                new_team_result = "Invalid team name \"%s\": name is longer than 50 characters." % new_team_name
            elif not team_exists(new_team_name):
                create_new_team_result = create_new_team(new_team_name,assigned_group)
                if not create_new_team_result:
                    new_team_result = "Failed to create team \"%s.\"" % new_team_name
                else:
                    new_team_result = new_team_name
            else:
                new_team_result = "Invalid team name \"%s\": name is already in use." % new_team_name
        else:
            new_team_result = None
        
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
    
    # Set the new list of teams after carrying out any creations or deletions.
    teams_and_groups = get_teams()
            
    return{
        "new_team_result": new_team_result,
        "groups": groups,
        "teams_deleted": teams_deleted,
        "teams_and_groups": teams_and_groups
    }
