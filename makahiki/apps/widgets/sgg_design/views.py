"""Provides the view of the widget."""
from apps.widgets.smartgrid.models import Level, Category, Activity, Event, Commitment
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from apps.widgets.smartgrid import smartgrid
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.context import RequestContext


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


@never_cache
@login_required
def view_action(request, action_type, slug):
    """individual action page"""
    action = smartgrid.get_action(slug=slug)
    user = request.user
    view_objects = {}

    action = smartgrid.annotate_action_details(user, action)

    return render_to_response("action.html", {
        "action": action,
        "display_form": True if "display_form" in request.GET else False,
        "view_objects": view_objects,
        }, context_instance=RequestContext(request))
