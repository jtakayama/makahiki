"""Provides the view of the widget."""

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
                # Assume games have unique names.
                current_game = GameInfo.objects.get(name=game)
                current_game.enabled = False
                current_game.save()
        # Enable disabled apps if checked
        if len(games_to_enable) > 0:
            for game in games_to_enable:
                # Assume that games have unique names.
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
                