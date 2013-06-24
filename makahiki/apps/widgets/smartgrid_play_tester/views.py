'''Provides the view functionality for the Smart Grid Play Tester.
Created on Jun 23, 2013

@author: Cam Moore
'''
from django.shortcuts import render_to_response
from apps.widgets.smartgrid_design.models import Draft
from django.template.context import RequestContext
from apps.managers.smartgrid_mgr import smartgrid_mgr
from django.http import Http404
from apps.widgets.smartgrid_play_tester import play_tester


def view(request):
    """Shows the Smart Grid Play Tester."""
    draft_choices = Draft.objects.all()
    try:
        draft_slug = request.COOKIES['current-designer-draft']
    except KeyError:
        draft_slug = draft_choices[0].slug
    try:
        draft = smartgrid_mgr.get_designer_draft(draft_slug)
    except Http404:
        draft = draft_choices[0]

    smart_grid = play_tester.get_designer_grid(draft)
    return render_to_response("play_tester.html", {
        "draft_choices": draft_choices,
        "smart_grid": smart_grid,
        }, context_instance=RequestContext(request))


def view_action(request, action_type, slug):
    """Shows the details of the action defined by the given action_type and slug."""
    pass


def add_action(request, action_type, slug):
    """Handles the play tester doing the action defined by the given action_type and slug."""
    pass


def drop_action(request, action_type, slug):
    """Handles the play tester dropping the given action defined by the action_type and slug."""
    pass
