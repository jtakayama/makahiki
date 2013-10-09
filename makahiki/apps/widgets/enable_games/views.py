"""Provides the view of the widget."""

from django.shortcuts import render_to_response
from django.shortcuts import render
#from django.http import HttpResponseRedirect

#games_enabled = None
#games_disabled = None


def supply(request, page_name):
    """ supply view_objects for widget rendering."""
    _ = request
    _ = page_name
    
    from apps.managers.challenge_mgr import challenge_mgr
    from apps.managers.challenge_mgr.models import GameInfo
    games_enabled = list(challenge_mgr.get_all_enabled_games())
    games_disabled = list(challenge_mgr.get_all_disabled_games())
    
    if request.method == 'POST':
        # Disable enabled apps if checked
        games_to_disable = request.POST.getlist("enabled_game[]")
        games_to_enable = request.POST.getlist("disabled_game[]")
        if len(games_to_disable) > 0:
            for game in games_to_disable:
                # This will cause an error if more than one object has the same name
                current_game = GameInfo.objects.get(name=game)
                current_game.enabled = False
                current_game.save()
        # Enable disabled apps if checked
        if len(games_to_disable) > 0:
            print "Execution check, remove when done."
            for game in games_to_enable:
                # This will cause an error if more than one object has the same name
                current_game = GameInfo.objects.get(name=game)
                current_game.enabled = True
                current_game.save()
        # Update values
        games_enabled = list(challenge_mgr.get_all_enabled_games())
        games_disabled = list(challenge_mgr.get_all_disabled_games())
    
    else:
        games_enabled = list(challenge_mgr.get_all_enabled_games())
        games_disabled = list(challenge_mgr.get_all_disabled_games())
    
    return{
        "games_enabled": games_enabled,
        "games_disabled": games_disabled
    }

#def supply(request, page_name):
#    """ supply view_objects for widget rendering."""
#    _ = request
#    _ = page_name
#    
#    from apps.managers.challenge_mgr.models import GameInfo
#    from django.forms.models import modelformset_factory
#    GameInfoFormSet = modelformset_factory(GameInfo, fields=('name','enabled'))
#    
#    if request.method == 'POST':
#        formset = GameInfoFormSet(request.POST, request.FILES,
#                                  queryset=GameInfo.objects.filter(enabled=True))
#        if formset.is_valid():
#            formset.save()
#    
#    else:
#        formset = GameInfoFormSet()

#    return render_to_response('quick_start.html', {"formset": formset})
    #return {"formset": formset,}
        #"games_enabled": games_enabled,
        #"games_disabled": games_disabled
    #}

#from django.forms import ModelForm
#from apps.managers.challenge_mgr.models import GameInfo
#from django.forms import CheckboxInput

#class SetGameInfoEnableForm(ModelForm):
#    is_enabled = list(challenge_mgr.get_all_enabled_games())
#    is_disabled = list(challenge_mgr.get_all_disabled_games())
#    
#    class Meta:
#        model = GameInfo
#        fields = ('name','enabled')
#        widgets = {
#            'enabled': CheckboxInput(check_test=None)
#        }

#form = SetGameInfoEnableForm()

# The below code did not work either.

# Need to change name - "contact" was the name used in the examples.
#def contact(request):
#    if request.method == 'POST':
#        #if request.form.isValid():
#        # Disable enabled apps if checked
#        for game in games_enabled:
#            if request.POST.get(game) == True:
#                # This will cause an error if more than one object has the same name
#                current_game = GameInfo.objects.get(name=game)
#                current_game.enabled = 'False'
#                current_game.save()
#        # Enable disabled apps if checked
#        for game in games_disabled:
#            if request.POST.get(game) == True:
#                # This will cause an error if more than one object has the same name
#                current_game = GameInfo.objects.get(name=game)
#                current_game.enabled = 'True'
#                current_game.save()
#        # Update values
#        games_enabled = list(challenge_mgr.get_all_enabled_games())
#        games_disabled = list(challenge_mgr.get_all_disabled_games())
#    # Not sure how to do return statement
#    return HttpResponseRedirect('.')
                