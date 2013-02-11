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
        'smart_grid': smartgrid.get_smart_grid(),
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

            num_levels = len(categories)
            for lvl in xrange(0, num_levels):
                level_cats = categories[lvl][1]
                for i in xrange(0, len(level_cats), 2):
                    category = Category.objects.get(slug=level_cats[i])
                    category.priority = level_cats[i + 1]
                    category.save()

            # clear the existing actions
            for action in Action.objects.all():
                action.category = None
                action.level = None
                action.save()

            num_levels = len(actions)
            for lvl in xrange(0, num_levels):
                level_name = actions[lvl][0]
                level = Level.objects.get(name=level_name)
                level_actions = actions[lvl][1]
                for i in xrange(0, len(level_actions), 3):
                    action = smartgrid.get_action(level_actions[i])
                    category = Category.objects.get(slug=level_actions[i + 1])
                    priority = level_actions[i + 2]
                    action.level = level
                    action.category = category
                    action.priority = priority
                    action.save()

            response = HttpResponseRedirect("/sgg_designer/")
            return response

    raise Http404
