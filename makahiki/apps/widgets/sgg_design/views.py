"""Provides the view of the widget."""
from apps.widgets.smartgrid.models import Level, Category, Activity, Event, Commitment, Action
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from apps.widgets.smartgrid import smartgrid
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from apps.widgets.sgg_design.forms import SggUpdateForm, ListFormField


def supply(request, page_name):
    """ supply view_objects for widget rendering."""
    _ = request
    _ = page_name
    levels = Level.objects.all()
    categories = Category.objects.all()
    activities = Activity.objects.all()
    events = Event.objects.all()
    commitments = Commitment.objects.all()
    form = SggUpdateForm({'category_updates': '[]',
                          'action_updates': '[]'})

    return {
        'levels': levels,
        'categories': categories,
        'activities': activities,
        'events': events,
        'commitments': commitments,
        'form': form,
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


def update_sgg(request):
    """Handles the SggUpdateForm from the 'Save SGG' button."""
    if request.method == "POST":
        form = SggUpdateForm(request.POST)
        if form.is_valid():
            categories = form.cleaned_data['category_updates']
            actions = form.cleaned_data['action_updates']

            for i in xrange(0, len(categories), 2):
                category = Category.objects.get(slug=categories[i])
                category.priority = categories[i + 1]
                category.save()

            for action in Action.objects.all():
                action.category = None
                action.save()

            for i in xrange(0, len(actions), 3):
                action = smartgrid.get_action(actions[i])
                category = Category.objects.get(slug=actions[i + 1])
                priority = actions[i + 2]
                action.category = category
                action.priority = priority
                action.save()

    raise Http404
