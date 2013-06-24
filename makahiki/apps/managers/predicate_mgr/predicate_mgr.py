'''Manager for predicates.
Created on Jun 15, 2013

@author: Cam Moore
'''

import sys
import inspect
from apps.managers.challenge_mgr.models import RoundSetting, GameInfo
from apps.widgets.smartgrid_library.models import LibraryEvent, LibraryAction
from apps.widgets.smartgrid_design.models import DesignerLevel, DesignerEvent, DesignerAction


# Used to build the unlock_conditions
(_AND, _OR, _NOT, _TRUE, _FALSE) = ('and', 'or', 'not', 'True', 'False')


def eval_predicates(predicates, user):
    """Returns the boolean evaluation result of the predicates against the user."""

    ALLOW_DICT = {"True": True, "False": False, "user": user}
    ALLOW_DICT.update(get_player_predicates())
    ALLOW_DICT.update(get_challenge_predicates())
    ALLOW_DICT.update(get_smartgrid_predicates())

    for key in ALLOW_DICT:
        if "%s(" % key in predicates:
            predicates = predicates.replace("%s(" % key, "%s(user," % key)

    return eval(predicates, {"__builtins__": None}, ALLOW_DICT)


def eval_play_tester_predicates(predicates, user):
    """Returns the boolean evaluation results of the tester predicates against the user."""
    ALLOW_DICT = {"True": True, "False": False, "user": user}
    ALLOW_DICT.update(get_player_tester_predicates())
    ALLOW_DICT.update(get_challenge_tester_predicates())
    ALLOW_DICT.update(get_smartgrid_tester_predicates())

    for key in ALLOW_DICT:
        if "%s(" % key in predicates:
            predicates = predicates.replace("%s(" % key, "%s(user," % key)

    return eval(predicates, {"__builtins__": None}, ALLOW_DICT)


def get_action_slugs(draft):
    """Returns a list of all the slugs available in the given draft.  This includes all the
    LibraryAction slugs and any new action slugs in the draft."""
    ret = get_library_action_slugs()
    for action in DesignerAction.objects.filter(draft=draft):
        if action.slug not in ret:
            ret.append(action.slug)
    return sorted(ret)


def get_action_types():
    """Returns a list of the possible action types."""
    return ('activity', 'commitment', 'event')


def get_challenge_predicates():
    """Returns the challenge predicates as a dictionary whose keys are the names of the predicates
    and the values are the predicate functions."""
    from apps.managers.predicate_mgr.challenge_predicates import game_enabled, reached_round
    return {
            "game_enabled": game_enabled,
            "reached_round": reached_round,
            }


def reached_round_tester():
    """Tester predicate replacement for challenge_mgr.predicates.reached_round."""
    return True


def get_challenge_tester_predicates():
    """Returns the tester challenge predicates."""
    from apps.managers.predicate_mgr.challenge_tester_predicates import game_enabled, reached_round
    return {
            "game_enabled": game_enabled,
            "reached_round": reached_round,
            }


def get_defined_predicates():
    """Returns the predicates defined in Makahiki as a dictionary."""
    ret = {}
    ret.update(get_player_predicates())
    ret.update(get_challenge_predicates())
    ret.update(get_smartgrid_predicates())
    return ret


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


def get_player_predicates():
    """Returns the predicates associated with players as a dictionary whose keys are the names
    of the predicates and values are the predicate functions."""
    from apps.managers.predicate_mgr.player_predicates import has_points, is_admin, \
    allocated_raffle_ticket, badge_awarded, posted_to_wall, set_profile_pic, daily_visit_count, \
    changed_theme, daily_energy_goal_count, referring_count, team_member_point_percent
    return {
            "is_admin": is_admin,
            "has_points": has_points,
            "allocated_raffle_ticket": allocated_raffle_ticket,
            "badge_awarded": badge_awarded,
            "posted_to_wall": posted_to_wall,
            "set_profile_pic": set_profile_pic,
            "daily_visit_count": daily_visit_count,
            "change_theme": changed_theme,
            "changed_theme": changed_theme,
            "daily_energy_goal_count": daily_energy_goal_count,
            "referring_count": referring_count,
            "team_member_point_percent": team_member_point_percent,
            }


def get_player_tester_predicates():
    """Returns the tester predicates associated with players.  This is the same
    get_player_predicates()."""
    return get_player_predicates()


def get_predicate_parameter_types(predicate_str):
    """Returns a list of the parameter types for the given predicate_str."""
    preds = get_defined_predicates()
    try:
        return inspect.getargspec(preds[predicate_str]).args
    except KeyError:
        return []


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


def get_smartgrid_predicates():  # pylint: disable=R0914
    """Returns the SmartGrid predicates as a dictionary whose keys are the names of the predicates
    and the values are the predicate functions."""
    from apps.managers.predicate_mgr.smartgrid_predicates import approved_action, \
    approved_all_of_level, approved_all_of_resource, approved_all_of_type, approved_some, \
    approved_some_full_spectrum, approved_some_of_level, approved_some_of_resource, \
    approved_some_of_type, completed_level, social_bonus_count, submitted_action, \
    submitted_all_of_level, submitted_all_of_resource, submitted_all_of_type, submitted_level, \
    submitted_some, submitted_some_full_spectrum, submitted_some_of_level, \
    submitted_some_of_resource, submitted_some_of_type, unlock_on_date, unlock_on_event

    return {
            "approved_action": approved_action,
            "approved_all_of_level": approved_all_of_level,
            "approved_all_of_resource": approved_all_of_resource,
            "approved_all_of_type": approved_all_of_type,
            "approved_some": approved_some,
            "approved_some_full_spectrum": approved_some_full_spectrum,
            "approved_some_of_level": approved_some_of_level,
            "approved_some_of_resource": approved_some_of_resource,
            "approved_some_of_type": approved_some_of_type,
            "completed_action": submitted_action,
            "completed_level": completed_level,
            "completed_some_of": submitted_some_of_type,
            "completed_some_of_level": submitted_some_of_level,
            "social_bonus_count": social_bonus_count,
            "submitted_action": submitted_action,
            "submitted_all_of_level": submitted_all_of_level,
            "submitted_all_of_resource": submitted_all_of_resource,
            "submitted_all_of_type": submitted_all_of_type,
            "submitted_level": submitted_level,
            "submitted_some": submitted_some,
            "submitted_some_full_spectrum": submitted_some_full_spectrum,
            "submitted_some_of_level": submitted_some_of_level,
            "submitted_some_of_resource": submitted_some_of_resource,
            "submitted_some_of_type": submitted_some_of_type,
            "unlock_on_date": unlock_on_date,
            "unlock_on_event": unlock_on_event,
            }  # pylint: enable=R0914


def get_smartgrid_tester_predicates():
    """Returns the tester smartgrid predicates."""
    from apps.managers.predicate_mgr.smartgrid_tester_predicates import approved_action, \
    approved_all_of_level, approved_all_of_resource, approved_all_of_type, approved_some, \
    approved_some_full_spectrum, approved_some_of_level, approved_some_of_resource, \
    approved_some_of_type, completed_level, social_bonus_count, submitted_action, \
    submitted_all_of_level, submitted_all_of_resource, submitted_all_of_type, submitted_level, \
    submitted_some, submitted_some_full_spectrum, submitted_some_of_level, \
    submitted_some_of_resource, submitted_some_of_type, unlock_on_date, unlock_on_event

    return {
            "approved_action": approved_action,
            "approved_all_of_level": approved_all_of_level,
            "approved_all_of_resource": approved_all_of_resource,
            "approved_all_of_type": approved_all_of_type,
            "approved_some": approved_some,
            "approved_some_full_spectrum": approved_some_full_spectrum,
            "approved_some_of_level": approved_some_of_level,
            "approved_some_of_resource": approved_some_of_resource,
            "approved_some_of_type": approved_some_of_type,
            "completed_action": submitted_action,
            "completed_level": completed_level,
            "completed_some_of": submitted_some_of_type,
            "completed_some_of_level": submitted_some_of_level,
            "social_bonus_count": social_bonus_count,
            "submitted_action": submitted_action,
            "submitted_all_of_level": submitted_all_of_level,
            "submitted_all_of_resource": submitted_all_of_resource,
            "submitted_all_of_type": submitted_all_of_type,
            "submitted_level": submitted_level,
            "submitted_some": submitted_some,
            "submitted_some_full_spectrum": submitted_some_full_spectrum,
            "submitted_some_of_level": submitted_some_of_level,
            "submitted_some_of_resource": submitted_some_of_resource,
            "submitted_some_of_type": submitted_some_of_type,
            "unlock_on_date": unlock_on_date,
            "unlock_on_event": unlock_on_event,
            }  # pylint: enable=R0914
    

def get_smartgrid_unlock_predicates():
    """Returns the suggested predicates for Smartgrid Action unlock conditions."""
    from apps.managers.predicate_mgr.smartgrid_predicates import approved_action, \
    submitted_action, unlock_on_date, unlock_on_event
    from apps.managers.predicate_mgr.player_predicates import has_points
    return {
            "submitted_action": submitted_action,
            "approved_action": approved_action,
            "has_points": has_points,
            "unlock_on_date": unlock_on_date,
            "unlock_on_event": unlock_on_event,
            }


def get_smartgrid_unlock_predicate_list():
    """Returns the suggested Smartgrid unlock condition predicate list."""
    ret = []
    ret.append('submitted_action')
    ret.append('approved_action')
    ret.append('has_points')
    ret.append('unlock_on_date')
    ret.append('unlock_on_event')
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


def is_predicate_name(name):
    """Returns True if the given name is a valid predicate function name."""
    predicates = get_defined_predicates()
    if name in predicates.keys():
        return True
    else:
        return False


def is_resource_predicate(predicate_fn):
    """Returns True if the predicate_fn takes a resource parameter."""
    return 'resource' in inspect.getargspec(predicate_fn).args


def is_round_name_predicate(predicate_fn):
    """Returns True if the predicate_fn takes a round_name parameter."""
    return 'round_name' in inspect.getargspec(predicate_fn).args


def validate_form_predicates(predicates):
    """validate the predicates in a form. if error, raise the form validation error."""
    from django import forms
    from django.contrib.auth.models import User

    # Pick a user and see if the conditions result is true or false.
    user = User.objects.all()[0]
    try:
        result = eval_predicates(predicates, user)
        # Check if the result type is a boolean
        if type(result) != type(True):
            raise forms.ValidationError("Expected boolean value but got %s" % type(result))
    except Exception:
        info = sys.exc_info()
        if len(info) > 1:
            raise forms.ValidationError("Received exception: %s:%s" % (sys.exc_info()[0],
                                        sys.exc_info()[1]))
        else:
            raise forms.ValidationError("Received exception: %s" % sys.exc_info()[0])


def validate_predicates(predicates):
    """Validate the predicates string."""
    from django.contrib.auth.models import User

    error_msg = None
    # Pick a user and see if the conditions result is true or false.
    user = User.objects.all()[0]
    try:
        result = eval_predicates(predicates, user)
        # Check if the result type is a boolean
        if type(result) != type(True):
            error_msg = "Expected boolean value but got %s" % type(result)
    except Exception:
        error_msg = "Received exception: %s" % sys.exc_info()[0]

    return error_msg
