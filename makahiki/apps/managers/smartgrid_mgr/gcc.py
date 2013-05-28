'''A checker for Draft Designer Smart Grids. Checks several different aspects of the grid and
reports Errors and Warnings.
Created on May 15, 2013

@author: Cam Moore
'''
from apps.managers.challenge_mgr import challenge_mgr
from apps.widgets.smartgrid_design.models import DesignerAction, DesignerEvent, DesignerGrid, \
    DesignerLevel, DesignerColumnGrid
from apps.managers.challenge_mgr.models import RoundSetting
from datetime import datetime, time
from apps.managers.smartgrid_mgr import smartgrid_mgr, action_dependency
import re
from apps.widgets.smartgrid_library.models import LibraryAction
import urllib2
from urllib2 import HTTPError, URLError
from apps.managers.smartgrid_mgr.gcc_model import Error, Warn, _ERRORS, _WARNINGS
from apps.utils import utils


def __is_in_round(date, roundsetting):
    """Returns True if the given date is in the given round."""
    return date >= roundsetting.start and date <= roundsetting.end


def __is_in_rounds(date):
    """Returns True if the given date is in any of the roundsettings."""
    ret = False
    for r in RoundSetting.objects.all():
        ret = ret or __is_in_round(date, r)
    return ret


def __is_in_challenge(date):
    """Returns True if the given date is between the Challenge start and end dates."""
    start = challenge_mgr.get_challenge_start()
    end = challenge_mgr.get_challenge_end()
    return date >= start and date <= end


def __is_after_challenge(date):
    """Returns True if the given date is after the Challenge end date."""
    return date > challenge_mgr.get_challenge_end()


def __is_boolean_logic(token):
    """Returns True if the token is boolean logic operator ('and', 'or', 'not') or ('True',
    'False')."""
    if token:
        return token.lower() in ['and', 'or', 'not', 'true', 'false']
    return False


def __get_urls(text):
    """Returns a list of the urls in the text."""
    ret = []
    urls = re.\
        findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', \
                 text.lower())
    for url in urls:
        if url.endswith(')') or url.endswith('>'):
            url = url[: -1]
        if url.endswith('),') or url.endswith(').'):
            url = url[: -2]
        if url.endswith(')</center'):
            url = url[: -9]
        ret.append(url)
    return ret


def __get_predicate(token):
    """Returns the predicate if any in the given token.  Predicates are defined as the string
    before '('.  e.g. the predicate in 'submitted_action(intro-video)' is submitted_action."""
    if token and token.find('(') != -1:
        return token[:token.find('(')]
    return None


def __check_predicates(action):
    """Checks the unlock_condition string of the given action ensuring that the predicates in the
    string are valid Makahiki predicates and that it has boolean logic only. Returns a list of
    Errors. Does not evaluate the predicates or test that the logic is correct."""
    ret = []
    unlock_condition = action.unlock_condition
    valid_predicates = utils.get_defined_predicates()
    if unlock_condition:
        pat = re.compile(r'([^(]+)\s*\(([^)]+)\)\s*')
        for pred, params in pat.findall(unlock_condition):
            _ = params
            for token in pred.split():
                if __is_boolean_logic(token):
                    pass
                else:
                    if token not in valid_predicates.keys():
                        message = "%s is not a defined Makahiki predicate" % token
                        ret.append(Error(message=message, action=action))
    return ret


def check_pub_exp_dates(draft):
    """Returns a dictionary of Errors and Warnings for DesignerActions whose pub_date or
     exp_date are not in the challenge."""
    ret = {}
    ret[_ERRORS] = []
    ret[_WARNINGS] = []
    challenge_start = challenge_mgr.get_challenge_start()
    challenge_end = challenge_mgr.get_challenge_end()
    for action in DesignerAction.objects.filter(draft=draft):
        if action.pub_date > challenge_end.date():
            ret[_ERRORS].append(Error(message="Publication Date after end of Challenge", \
                                       action=action))
        if action.expire_date and \
            datetime.combine(action.expire_date, time(0, 0)) < \
            challenge_start.date():
            ret[_ERRORS].append(Error(message="Expiration date before beginning of Challenge", \
                                       action=action))
        if not __is_in_rounds(datetime.combine(action.pub_date, time(0, 0))):
            ret[_WARNINGS].append(Warn(message="Publication Date isn't in a round", \
                                        action=action))
        if action.expire_date and not \
            __is_in_rounds(datetime.combine(action.expire_date, time(0, 0))):
            ret[_WARNINGS].append(Warn(message="Expiration Date isn't in a round", \
                                        action=action))
    return ret


def check_grid_pub_exp_dates(draft):
    """Returns a dictionary of Errors and Warnings for DesignerActions in the grid whose pub_date or
     exp_date are not in the challenge."""
    ret = {}
    ret[_ERRORS] = []
    ret[_WARNINGS] = []
    challenge_start = challenge_mgr.get_challenge_start()
    challenge_end = challenge_mgr.get_challenge_end()
    for loc in DesignerGrid.objects.filter(draft=draft):
        if loc.action.pub_date > challenge_end.date():
            message = "Publication Date %s after end of Challenge %s" % (loc.action.pub_date, \
                                                                         challenge_end.date())
            ret[_ERRORS].append(Error(message=message, \
                                       action=loc.action))
        if loc.action.expire_date and \
            loc.action.expire_date < \
            challenge_start.date():
            message = "Expiration date %s is before beginning of Challenge %s" % \
            (loc.action.expire_date, challenge_start.date())
            ret[_ERRORS].append(Error(message=message, \
                                       action=loc.action))
#         if not __is_in_rounds(datetime.combine(loc.action.pub_date, time(0, 0))):
#             message = "Publication Date %s isn't in a round" % loc.action.pub_date
#             ret[_WARNINGS].append(Warn(message=message, \
#                                         action=loc.action))
#         if loc.action.expire_date and not \
#             __is_in_rounds(datetime.combine(loc.action.expire_date, time(0, 0))):
#             message = "Expiration Date isn't in a round" % loc.action.expire_date
#             ret[_WARNINGS].append(Warn(message=message, \
#                                         action=loc.action))
    return ret


def check_event_dates(draft):
    """Returns a list of Errors for DesignerEvents whose event_date isn't in the challenge or
    isn't during a round."""
    ret = []
    for event in DesignerEvent.objects.filter(draft=draft):
        if not __is_in_rounds(event.event_date):
            ret.append(Error(message="Event date isn't in a round", action=event))
        if not __is_in_challenge(event.event_date):
            ret.append(Error(message="Event date isn't in the challenge", action=event))
    return ret


def check_grid_event_dates(draft):
    """Returns a list of Errors for DesignerEvents in the grid whose event_date isn't in the
    challenge or isn't during a round."""
    ret = []
    for loc in DesignerGrid.objects.filter(draft=draft):
        if loc.action.type == 'event':
            event = smartgrid_mgr.get_designer_action(draft=draft, slug=loc.action.slug)
            if not __is_in_rounds(event.event_date):
                message = "Event date %s isn't in a round" % event.event_date.date()
                ret.append(Error(message=message, action=event))
            if not __is_in_challenge(event.event_date):
                message = "Event date %s isn't in the challenge %s - %s" % \
                (event.event_date.date(), challenge_mgr.get_challenge_start().date(), \
                 challenge_mgr.get_challenge_end().date())
                ret.append(Error(message=message, action=event))
    return ret


def check_designer_unlock_dates(draft):
    """Checks all the DesignerAction unlock_conditions looking for unlock_on_date predicates.
    Checks the dates in the predicate to ensure they are in the challenge."""
    ret = {}
    ret[_ERRORS] = []
    ret[_WARNINGS] = []
    for action in DesignerAction.objects.filter(draft=draft):
        if action.unlock_condition:
            l = action.unlock_condition.split('unlock_on_date(')
            if len(l) > 1:
                index = l[1].find(')')
                date_string = l[1][:index].strip('"\'')
                unlock_date = datetime.strptime(date_string, "%m/%d/%y")
                if __is_after_challenge(datetime.combine(unlock_date, time(0, 0))):
                    message = "unlock date %s is after challenge end %s" % \
                    (unlock_date.date(), challenge_mgr.get_challenge_end().date())
                    ret[_ERRORS].append(Error(message=message, action=action))
                if not __is_in_rounds(datetime.combine(unlock_date, time(0, 0))):
                    message = "unlock date %s is not in a round" % unlock_date.date()
                    ret[_WARNINGS].append(Warn(message=message, \
                                                action=action))

    return ret


def check_designer_urls(draft):
    """Checks all the DesignerAction descriptions looking for URLs and checks that they return a
    valid HTTP status code. If they don't a warning is appended to the list of warnings."""
    ret = []
    for action in DesignerAction.objects.filter(draft=draft):
        urls = __get_urls(action.description)
        for url in urls:
            req = urllib2.Request(url)
            try:
                urllib2.urlopen(req)
            except HTTPError as e:
                msg = "url %s raised error %s" % (url, e)
                ret.append(Warn(message=msg, action=action))
            except URLError as e1:
                msg = "url %s raised error %s" % (url, e1)
                ret.append(Warn(message=msg, action=action))
    return ret


def check_designer_predicates(draft):
    """Checks the Designer items' unlock_condition ensuring the predicates are defined.  This does
    not evaluate the predicates, just ensures that the predicates are defined."""
    ret = []
    for action in DesignerAction.objects.filter(draft=draft):
        for issue in __check_predicates(action):
            ret.append(issue)
    for level in DesignerLevel.objects.filter(draft=draft):
        for issue in __check_predicates(level):
            ret.append(issue)
    return ret


def check_designer_action_column_names(draft):
    """Checks for actions in columns that don't have a column name."""
    ret = []
    for grid in DesignerGrid.objects.filter(draft=draft):
        if len(DesignerColumnGrid.objects.filter(draft=draft, level=grid.level, \
                                                 column=grid.column)) == 0:
            message = "in %s column %s row %s needs a column name." % (grid.level, \
                                                                       grid.column, \
                                                                       grid.row)
            ret.append(Error(message=message, action=grid.action))
        grid.column
    return ret


def check_unreachable_designer_actions(draft):
    """Checks for unreachable actions and returns a list of Errors indicating which actions are
    unreachable."""
    return action_dependency.check_unreachable_designer_actions(draft)


def check_false_unlock_conditions(draft):
    """Checks for actions that depend on actions with False unlock_conditions."""
    return action_dependency.check_false_unlock_designer_actions(draft)


def check_mismatched_designer_level(draft):
    """Checks for actions that depend on actions in a higher level."""
    return action_dependency.check_missmatched_designer_level(draft)


def run_designer_checks(draft, settings):  # pylint: disable=R0912
    """Runs the checks that the user set in their GccSettings."""
    ret = {}
    ret[_ERRORS] = []
    ret[_WARNINGS] = []
    # cannot turn off checking the predicates.
    for e in check_designer_predicates(draft):
        ret[_ERRORS].append(str(e))
    for e in check_designer_action_column_names(draft):
        ret[_ERRORS].append(str(e))
    if settings.check_pub_dates:
        d = check_grid_pub_exp_dates(draft)
        for e in d[_ERRORS]:
            ret[_ERRORS].append(str(e))
        for w in d[_WARNINGS]:
            ret[_WARNINGS].append(str(w))
    if settings.check_event_dates:
        d = check_grid_event_dates(draft)
        for e in d:
            ret[_ERRORS].append(str(e))
    if settings.check_unlock_dates:
        d = check_designer_unlock_dates(draft)
        for e in d[_ERRORS]:
            ret[_ERRORS].append(str(e))
        for w in d[_WARNINGS]:
            ret[_WARNINGS].append(str(w))
    if settings.check_description_urls:
        for w in check_designer_urls(draft):
            ret[_WARNINGS].append(str(w))
    if settings.check_unreachable:
        for e in action_dependency.check_unreachable_designer_actions(draft):
            ret[_ERRORS].append(str(e))
    if settings.check_false_unlocks:
        for w in action_dependency.check_false_unlock_designer_actions(draft):
            ret[_WARNINGS].append(str(w))
    if settings.check_mismatched_levels:
        for w in action_dependency.check_missmatched_designer_level(draft):
            ret[_WARNINGS].append(str(w))
    return ret
# pylint: enable=R0912


def full_designer_check(draft):
    """Runs all the designer checks (slow)."""
    ret = {}
    ret[_ERRORS] = []
    ret[_WARNINGS] = []
    d = check_pub_exp_dates(draft)
    for e in d[_ERRORS]:
        ret[_ERRORS].append(str(str(e)))
    for w in d[_WARNINGS]:
        ret[_WARNINGS].append(str(w))
    d = check_grid_pub_exp_dates(draft)
    for e in d[_ERRORS]:
        ret[_ERRORS].append(str(e))
    for w in d[_WARNINGS]:
        ret[_WARNINGS].append(str(w))
    d = check_event_dates(draft)
    for e in d:
        ret[_ERRORS].append(str(e))
    d = check_grid_event_dates(draft)
    for e in d:
        ret[_ERRORS].append(str(e))
    d = check_designer_unlock_dates(draft)
    for e in d[_ERRORS]:
        ret[_ERRORS].append(str(e))
    for w in d[_WARNINGS]:
        ret[_WARNINGS].append(str(w))
    for w in check_designer_urls(draft):
        ret[_WARNINGS].append(str(w))
    for e in action_dependency.check_unreachable_designer_actions(draft):
        ret[_ERRORS].append(str(e))
    for w in action_dependency.check_false_unlock_designer_actions(draft):
        ret[_WARNINGS].append(str(w))
    for w in action_dependency.check_missmatched_designer_level(draft):
        ret[_WARNINGS].append(str(w))
    return ret


def quick_designer_check(draft):
    """Quick test."""
    ret = {}
    ret[_ERRORS] = []
    ret[_WARNINGS] = []
    d = check_grid_pub_exp_dates(draft)
    for e in d[_ERRORS]:
        ret[_ERRORS].append(str(e))
    for w in d[_WARNINGS]:
        ret[_WARNINGS].append(str(w))
    d = check_grid_event_dates(draft)
    for e in d:
        ret[_ERRORS].append(str(e))
    d = check_designer_unlock_dates(draft)
    for e in d[_ERRORS]:
        ret[_ERRORS].append(str(e))
    for w in d[_WARNINGS]:
        ret[_WARNINGS].append(str(w))
    for e in action_dependency.check_unreachable_designer_actions(draft):
        ret[_ERRORS].append(str(e))
    for w in action_dependency.check_false_unlock_designer_actions(draft):
        ret[_WARNINGS].append(str(w))
    for w in action_dependency.check_missmatched_designer_level(draft):
        ret[_WARNINGS].append(str(w))
    return ret


def check_library_unlock_dates():
    """Checks all the LibraryAction unlock_conditions looking for unlock_on_date predicates.
    Checks the dates in the predicate to ensure they are in the challenge."""
    ret = {}
    ret[_ERRORS] = []
    ret[_WARNINGS] = []
    for action in LibraryAction.objects.all():
        l = action.unlock_condition.split('unlock_on_date(')
        if len(l) > 1:
            index = l[1].find(')')
            date_string = l[1][:index].strip('"\'')
            unlock_date = datetime.strptime(date_string, "%m/%d/%y")
            if not __is_in_challenge(datetime.combine(unlock_date, time(0, 0))):
                ret[_ERRORS].append(Error(message="unlock date is not in challenge", \
                                           action=action))
            if not __is_in_rounds(datetime.combine(unlock_date, time(0, 0))):
                ret[_WARNINGS].append(Warn(message="unlock date is not in a round", \
                                            action=action))

    return ret


def check_library_urls():
    """Checks all the LibraryAction descriptions looking for URLs and checks that they return a
    valid HTTP status code. If they don't a warning is raised. Returns a list of Warnings."""
    ret = []
    for action in LibraryAction.objects.all():
        urls = __get_urls(action.description)
        for url in urls:
            req = urllib2.Request(url)
            try:
                urllib2.urlopen(req)
            except HTTPError as e:
                msg = "url %s raised error %s" % (url, e)
                ret.append(Warn(message=msg, action=action))
            except URLError as e1:
                msg = "url %s raised error %s" % (url, e1)
                ret.append(Warn(message=msg, action=action))
    return ret


def check_library_predicates():
    """Checks all the Library items' predicates."""
    ret = []
    for action in LibraryAction.objects.all():
        for issue in __check_predicates(action):
            ret.append(issue)
    return ret


def full_library_check():
    """Runs all the consistency checks on the library returning a dictionary with the Errors and
    Warnings."""
    ret = {}
    ret[_ERRORS] = []
    ret[_WARNINGS] = []
    d = check_library_unlock_dates()
    for e in d[_ERRORS]:
        ret[_ERRORS].append(str(e))
    for w in d[_WARNINGS]:
        ret[_WARNINGS].append(str(w))
    for w in check_library_urls():
        ret[_WARNINGS].append(str(w))
    for e in action_dependency.check_unreachable_library_actions():
        ret[_ERRORS].append(str(e))
    for w in action_dependency.check_false_unlock_library_actions():
        ret[_WARNINGS].append(str(w))
    return ret


def quick_library_check():
    """Runs the faster checks, not urls."""
    ret = {}
    ret[_ERRORS] = []
    ret[_WARNINGS] = []
    d = check_library_unlock_dates()
    for e in d[_ERRORS]:
        ret[_ERRORS].append(str(e))
    for w in d[_WARNINGS]:
        ret[_WARNINGS].append(str(w))
    for e in action_dependency.check_unreachable_library_actions():
        ret[_ERRORS].append(str(e))
    for w in action_dependency.check_false_unlock_library_actions():
        ret[_WARNINGS].append(str(w))
    return ret


def library_errors():
    """Returns the errors found in the Library items."""
    ret = quick_library_check()
    return ret[_ERRORS]
