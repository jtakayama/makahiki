"""Provides the view of the widget."""


def supply(request, page_name):
    """ supply view_objects for widget rendering."""
    _ = request
    _ = page_name
    games = request.game.get_all()
    return {
        "games": games,
    }
