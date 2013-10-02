"""Provides the view of the widget."""

import apps.managers.challenge_mgr.challenge_mgr as challenge_mgr

def supply(request, page_name):
    """ supply view_objects for widget rendering."""
    _ = request
    _ = page_name
    games_enabled = list(challenge_mgr.get_all_enabled_games())
    games_disabled = list(challenge_mgr.get_all_disabled_games())
    
    return {
        "games_enabled": games_enabled,
        "games_disabled": games_disabled
    }
