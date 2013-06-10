'''Helps the Smartgrid Designer build correct unlock_conditions by allowing them to choose from
valid choices not just type into the unlock_codition text field.
Created on May 30, 2013

@author: Cam Moore
'''
from apps.widgets.smartgrid_library.models import LibraryAction, LibraryEvent
from apps.widgets.smartgrid_design.models import DesignerAction, DesignerEvent, DesignerLevel
import inspect
from apps.utils import utils
from apps.managers.challenge_mgr.models import GameInfo, RoundSetting


# Used to build the unlock_conditions
(_AND, _OR, _NOT, _TRUE, _FALSE) = ('and', 'or', 'not', 'True', 'False')


def get_action_slugs(draft):
    """Returns a list of all the slugs available in the given draft.  This includes all the
    LibraryAction slugs and any new action slugs in the draft."""
    ret = get_library_action_slugs()
    for action in DesignerAction.objects.filter(draft=draft):
        if action.slug not in ret:
            ret.append(action.slug)
    return ret


def get_action_types():
    """Returns a list of the possible action types."""
    return ('activity', 'commitment', 'event')


def get_event_slugs(draft):
    """Returns a list of all the Event slugs available in the given draft."""
    ret = get_library_event_slugs()
    for event in DesignerEvent.objects.filter(draft=draft):
        if event.slug not in ret:
            ret.append(event.slug)
    return ret


def get_game_names():
    """Returns a list of all the game names."""
    ret = []
    for info in GameInfo.objects.all():
        if info.name not in ret:
            ret.append(info.name)
    return ret


def get_level_names(draft):
    """Returns a list of all the level names defined in the given draft."""
    ret = []
    for level in DesignerLevel.objects.filter(draft=draft):
        if level.name not in ret:
            ret.append(level.name)
    return ret


def get_library_action_slugs():
    """Returns a list of the LibraryAction slugs."""
    ret = []
    for action in LibraryAction.objects.all():
        if action.slug not in ret:
            ret.append(action.slug)
    return ret


def get_library_event_slugs():
    """Returns a list of all the LibraryEvent slugs."""
    ret = []
    for event in LibraryEvent.objects.all():
        if event.slug not in ret:
            ret.append(event.slug)
    return ret


def get_resources():
    """Returns a list of the possible resource choices."""
    return ('energy', 'water', 'waste')


def get_round_names():
    """Returns a list of the defined round names."""
    ret = []
    for r in RoundSetting.objects.all():
        if r.name not in ret:
            ret.append(r.name)
    return ret


def is_action_slug_predicate(predicate_fn):
    """Returns true if the predicate_fn takes parameter that is an Action slug."""
    return 'action_slug' in inspect.getargspec(predicate_fn).args


def is_action_type_predicate(predicate_fn):
    """Returns True if the predicate_fn takes an action_type parameter."""
    return 'action_type' in inspect.getargspec(predicate_fn).args


def is_event_slug_predicate(predicate_fn):
    """Returns True if the predicated_fn takes a parameter that is an event_slug."""
    return 'event_slug' in inspect.getargspec(predicate_fn).args


def is_game_name_predicate(predicate_fn):
    """Returns True if the predicate_fn takes a game_name parameter."""
    return 'game_name' in inspect.getargspec(predicate_fn).args


def is_level_name_predicate(predicate_fn):
    """Returns True if the predicate_fn takes a level_name parameter."""
    return 'level_name' in inspect.getargspec(predicate_fn).args


def is_resource_predicate(predicate_fn):
    """Returns True if the predicate_fn takes a resource parameter."""
    return 'resource' in inspect.getargspec(predicate_fn).args


def is_round_name_predicate(predicate_fn):
    """Returns True if the predicate_fn takes a round_name parameter."""
    return 'round_name' in inspect.getargspec(predicate_fn).args


def get_choices(predicate_str, draft):
    """Returns the choices for the predicate_str."""
    preds = utils.get_defined_predicates()
    ret = []
    try:
        pred = preds[predicate_str]
        if is_action_slug_predicate(pred):
            ret = get_action_slugs(draft=draft)
        if is_action_type_predicate(pred):
            ret = get_action_types()
        if is_event_slug_predicate(pred):
            ret = get_event_slugs(draft=draft)
        if is_game_name_predicate(pred):
            ret = get_game_names()
        if is_level_name_predicate(pred):
            ret = get_level_names(draft=draft)
        if is_resource_predicate(pred):
            ret = get_resources()
        if is_round_name_predicate(pred):
            ret = get_round_names()
    except KeyError:
        pass
    return ret


def get_predicate_parameter_types(predicate_str):
    """Returns a list of the parameter types for the given predicate_str."""
    preds = utils.get_defined_predicates()
    try:
        return inspect.getargspec(preds[predicate_str]).args
    except KeyError:
        return []


def get_predicate_list():
    """Returns an ordered list of the available predicates."""
    ret = []
    ret.append('submitted_action')
    ret.append('submitted_some_of_type')
    ret.append('unlock_on_date')
    ret.append('reached_round')
    ret.append('unlock_on_event')
    ret.append('approved_action')
    ret.append('approved_some_of_type')
    ret.append('submitted_some_of_level')
    ret.append('approved_some_of_level')
    ret.append('completed_level')
    ret.append('submitted_level')
    for pred in list(utils.get_defined_predicates()):
        if pred not in ret:
            ret.append(pred)
    return ret
