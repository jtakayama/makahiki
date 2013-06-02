'''Helps the Smartgrid Designer build correct unlock_conditions by allowing them to choose from
valid choices not just type into the unlock_codition text field.
Created on May 30, 2013

@author: Cam Moore
'''
from apps.widgets.smartgrid_library.models import LibraryAction, LibraryEvent
from apps.widgets.smartgrid_design.models import DesignerAction, DesignerEvent, DesignerLevel
import inspect
from apps.utils import utils


# Used to build the unlock_conditions
(_AND, _OR, _NOT, _TRUE, _FALSE) = ('and', 'or', 'not', 'True', 'False')


def __get_library_action_slugs():
    """Returns a list of the LibraryAction slugs."""
    ret = []
    for action in LibraryAction.objects.all():
        if action.slug not in ret:
            ret.append(action.slug)
    return ret


def __get_library_event_slugs():
    """Returns a list of all the LibraryEvent slugs."""
    ret = []
    for event in LibraryEvent.objects.all():
        if event.slug not in ret:
            ret.append(event.slug)
    return ret


def __get_action_slugs(draft):
    """Returns a list of all the slugs available in the given draft.  This includes all the
    LibraryAction slugs and any new action slugs in the draft."""
    ret = __get_library_action_slugs()
    for action in DesignerAction.objects.filter(draft=draft):
        if action.slug not in ret:
            ret.append(action.slug)
    return ret


def __get_event_slugs(draft):
    """Returns a list of all the Event slugs available in the given draft."""
    ret = __get_library_event_slugs()
    for event in DesignerEvent.objects.filter(draft=draft):
        if event.slug not in ret:
            ret.append(event.slug)
    return ret


def __get_level_names(draft):
    """Returns a list of all the level names defined in the given draft."""
    ret = []
    for level in DesignerLevel.objects.filter(draft=draft):
        if level.name not in ret:
            ret.append(level.name)
    return ret


def __get_resources():
    """Returns a list of the possible resource choices."""
    return ('energy', 'water', 'waste')


def __get_action_types():
    """Returns a list of the possible action types."""
    return ('activity', 'commitment', 'event')


def __is_action_slug_predicate(predicate_fn):
    """Returns true if the predicate_fn takes parameter that is an Action slug."""
    return 'slug' in inspect.getargspec(predicate_fn).args


def __is_event_slug_predicate(predicate_fn):
    """Returns True if the predicated_fn takes a parameter that is an event_slug."""
    return 'event_slug' in inspect.getargspec(predicate_fn).args


def __is_resource_predicate(predicate_fn):
    """Returns True if the predicate_fn takes a resource parameter."""
    return 'resource' in inspect.getargspec(predicate_fn).args


def __is_action_type_predicate(predicate_fn):
    """Returns True if the predicate_fn takes an action_type parameter."""
    return 'action_type' in inspect.getargspec(predicate_fn).args


def __is_level_name_predicate(predicate_fn):
    """Returns True if the predicate_fn takes a level_name parameter."""
    return 'level_name' in inspect.getargspec(predicate_fn).args


def get_choices(predicate_str, draft):
    """Returns the choices for the predicate_str."""
    preds = utils.get_defined_predicates()
    try:
        pred = preds[predicate_str]
        if __is_action_slug_predicate(pred):
            return __get_action_slugs(draft=draft)
        if __is_event_slug_predicate(pred):
            return __get_event_slugs(draft=draft)
        if __is_resource_predicate(pred):
            return __get_resources()
        if __is_action_type_predicate(pred):
            return __get_action_types()
        if __is_level_name_predicate(pred):
            return __get_level_names(draft=draft)
    except KeyError:
        return []
    return []
