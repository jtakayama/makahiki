'''Provides the view for the Unlock Condition Creator widget.
Created on Jun 5, 2013

@author: Cam Moore
'''
from apps.managers.smartgrid_mgr import smartgrid_mgr
from apps.widgets.smartgrid_design.models import Draft
from django.http import Http404, HttpResponse
import json
from apps.managers.predicate_mgr import predicate_mgr


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
        "predicates": predicate_mgr.get_smartgrid_unlock_predicate_list(),
        "action_slugs": predicate_mgr.get_action_slugs(draft=draft),
        "action_types": predicate_mgr.get_action_types(),
        "event_slugs": predicate_mgr.get_event_slugs(draft=draft),
        "game_names": predicate_mgr.get_game_names(),
        "level_names": predicate_mgr.get_level_names(draft=draft),
        "resources": predicate_mgr.get_resources(),
        "round_names": predicate_mgr.get_round_names(),
        }


def predicate_parameters(request, predicate):
    """Returns the names of the parameters for the given predicate."""
    _ = request
    parameters = predicate_mgr.get_predicate_parameter_types(predicate)
    return HttpResponse(json.dumps({
            "parameters": parameters,
            }), mimetype="application/json")
