'''Provides the view functionality for the Smart Grid Play Tester.
Created on Jun 23, 2013

@author: Cam Moore
'''
from django.shortcuts import render_to_response
from apps.widgets.smartgrid_design.models import Draft
from django.template.context import RequestContext
from apps.managers.smartgrid_mgr import smartgrid_mgr
from django.http import Http404, HttpResponseRedirect
from apps.widgets.smartgrid_play_tester import play_tester, view_test_commitments,\
    view_test_activities, view_test_events
from django.core.urlresolvers import reverse
from django.utils import importlib


def view(request):
    """Shows the Smart Grid Play Tester."""
    user = request.user
    draft_choices = Draft.objects.all()
    draft = _get_current_draft(request)
    smart_grid = play_tester.get_designer_grid(draft=draft, user=user)
    return render_to_response("play_tester.html", {
        "draft_choices": draft_choices,
        "draft": draft,
        "levels": smartgrid_mgr.get_designer_test_levels(draft=draft, user=user),
        "smart_grid": smart_grid,
        }, context_instance=RequestContext(request))


def view_action(request, action_type, slug):
    """Shows the details of the action defined by the given action_type and slug."""
    draft = _get_current_draft(request)
    user = request.user
    view_objects = {}
    action = smartgrid_mgr.get_designer_action(draft=draft, slug=slug)
    action = play_tester.annotate_action_details(user, action)

    if not action.is_unlock:
        response = HttpResponseRedirect(reverse("tester_view", args=()))
        response.set_cookie("task_unlock_condition", action.unlock_condition_text)
        return response

    if action_type == "commitment":
        form = view_test_commitments.view(request, action)
    elif action_type == "activity":
        form = view_test_activities.view(request, action)

        # if there is embedded widget, get the supplied objects
        if action.embedded_widget:
            view_module_name = 'apps.widgets.' + action.embedded_widget + '.views'
            view_objects[action.embedded_widget] = importlib.import_module(
                view_module_name).supply(request, None)
            view_objects['embedded_widget_template'] = "widgets/" + \
                action.embedded_widget + "/templates/index.html"
    elif action.type in ("event",):  # action.event:
        form = view_test_events.view(request, action)
        # calculate available seat
        action.available_seat = action.event.event_max_seat - 1
    elif action_type == "filler":
        response = HttpResponseRedirect(reverse("tester_view", args=()))
        return response

    feedback = None

    return render_to_response("tester_action.html", {
        "action": action,
        "form": form,
        "completed_count": 1,
        "team_members": [],
        "display_form": True if "display_form" in request.GET else False,
        "reminders": None,
        "view_objects": view_objects,
        "feedback_p": feedback,
        }, context_instance=RequestContext(request))


def add_action(request, action_type, slug):
    """Handles the play tester doing the action defined by the given action_type and slug."""
    draft = _get_current_draft(request)
    action = smartgrid_mgr.get_designer_action(draft=draft, slug=slug)
    if action_type == "commitment":
        return view_test_commitments.add(request, action)
    elif action_type == "activity":
        return view_test_activities.add(request, action)
    else:       # event
        return view_test_events.add(request, action)


def drop_action(request, action_type, slug):
    """Handles the play tester dropping the given action defined by the action_type and slug."""
    pass


def _get_current_draft(request):
    """Returns the currently selected Draft."""
    draft_choices = Draft.objects.all()
    try:
        draft_slug = request.COOKIES['current-designer-draft']
    except KeyError:
        draft_slug = draft_choices[0].slug
    try:
        draft = smartgrid_mgr.get_designer_draft(draft_slug)
    except Http404:
        draft = draft_choices[0]
    return draft
