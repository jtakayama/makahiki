'''Provides the view for the Unlock Condition Creator widget.
Created on Jun 5, 2013

@author: Cam Moore
'''
from apps.managers.smartgrid_mgr import unlock_creator, smartgrid_mgr
from apps.widgets.smartgrid_design.models import Draft
from django.http import Http404, HttpResponse
import json


def supply(request, page_name):
    """Supplies view_objects for smartgrid library widgets."""
    _ = page_name
    _ = request

    draft_choices = Draft.objects.all()
    draft = None
    try:
        draft_slug = request.REQUEST['draft']
    except KeyError:
        try:
            draft_slug = request.COOKIES['current-designer-draft']
        except KeyError:
            draft_slug = draft_choices[0].slug
    try:
        draft = smartgrid_mgr.get_designer_draft(draft_slug)
    except Http404:
        if len(draft_choices) > 0:
            draft = draft_choices[0]

    return {
        "predicates": unlock_creator.get_predicate_list(),
        "action_slugs": unlock_creator.get_action_slugs(draft=draft),
        "action_types": unlock_creator.get_action_types(),
        "event_slugs": unlock_creator.get_event_slugs(draft=draft),
        "game_names": unlock_creator.get_game_names(),
        "level_names": unlock_creator.get_level_names(draft=draft),
        "resources": unlock_creator.get_resources(),
        "round_names": unlock_creator.get_round_names(),
        }


def predicate_parameters(request, predicate):
    """Returns the names of the parameters for the given predicate."""
    _ = request
    parameters = unlock_creator.get_predicate_parameter_types(predicate)
    return HttpResponse(json.dumps({
            "parameters": parameters,
            }), mimetype="application/json")
