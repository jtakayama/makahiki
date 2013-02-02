"""Provides the view of the widget."""
from apps.widgets.smartgrid.models import Level, Category, Activity, Event, Commitment


def supply(request, page_name):
    """ supply view_objects for widget rendering."""
    _ = request
    _ = page_name
    levels = Level.objects.all()
    categories = Category.objects.all()
    activities = Activity.objects.all()
    events = Event.objects.all()
    commitments = Commitment.objects.all()

    return {
        'levels': levels,
        'categories': categories,
        'activities': activities,
        'events': events,
        'commitments': commitments,
            }
