'''A checker for Draft Designer Smart Grids. Checks several different aspects of the grid and
reports Errors and Warnings.
Created on May 15, 2013

@author: Carm Moore
'''
from apps.managers.challenge_mgr import challenge_mgr
from apps.widgets.smartgrid_design.models import DesignerAction, DesignerEvent, DesignerGrid
from apps.managers.challenge_mgr.models import RoundSetting
from datetime import datetime, time
from apps.managers.smartgrid_mgr import smartgrid_mgr, action_dependency
import re
from apps.widgets.smartgrid_library.models import LibraryAction
import urllib2
from urllib2 import HTTPError, URLError
from apps.managers.smartgrid_mgr.gcc_model import Error, Warn


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


def check_pub_exp_dates(draft):
    """Returns a dictionary of Errors and Warnings for DesignerActions whose pub_date or
     exp_date are not in the challenge."""
    ret = {}
    ret['errors'] = []
    ret['warnings'] = []
    challenge_start = challenge_mgr.get_challenge_start()
    challenge_end = challenge_mgr.get_challenge_end()
    for action in DesignerAction.objects.filter(draft=draft):
        if action.pub_date > challenge_end.date():
            ret['errors'].append(Error(message="Publication Date after end of Challenge", \
                                       action=action))
        if action.expire_date and \
            datetime.combine(action.expire_date, time(0, 0)) < \
            challenge_start.date():
            ret['errors'].append(Error(message="Expiration date before beginning of Challenge", \
                                       action=action))
        if not __is_in_rounds(datetime.combine(action.pub_date, time(0, 0))):
            ret['warnings'].append(Warn(message="Publication Date isn't in a round", \
                                        action=action))
        if action.expire_date and not \
            __is_in_rounds(datetime.combine(action.expire_date, time(0, 0))):
            ret['warnings'].append(Warn(message="Expiration Date isn't in a round", \
                                        action=action))
    return ret


def check_grid_pub_exp_dates(draft):
    """Returns a dictionary of Errors and Warnings for DesignerActions in the grid whose pub_date or
     exp_date are not in the challenge."""
    ret = {}
    ret['errors'] = []
    ret['warnings'] = []
    challenge_start = challenge_mgr.get_challenge_start()
    challenge_end = challenge_mgr.get_challenge_end()
    for loc in DesignerGrid.objects.filter(draft=draft):
        if loc.action.pub_date > challenge_end.date():
            ret['errors'].append(Error(message="Publication Date after end of Challenge", \
                                       action=loc.action))
        if loc.action.expire_date and \
            datetime.combine(loc.action.expire_date, time(0, 0)) < \
            challenge_start.date():
            ret['errors'].append(Error(message="Expiration date before beginning of Challenge", \
                                       action=loc.action))
        if not __is_in_rounds(datetime.combine(loc.action.pub_date, time(0, 0))):
            ret['warnings'].append(Warn(message="Publication Date isn't in a round", \
                                        action=loc.action))
        if loc.action.expire_date and not \
            __is_in_rounds(datetime.combine(loc.action.expire_date, time(0, 0))):
            ret['warnings'].append(Warn(message="Expiration Date isn't in a round", \
                                        action=loc.action))
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
                ret.append(Error(message="Event date isn't in a round", action=event))
            if not __is_in_challenge(event.event_date):
                ret.append(Error(message="Event date isn't in the challenge", action=event))
    return ret


def check_designer_unlock_dates(draft):
    """Checks all the DesignerAction unlock_conditions looking for unlock_on_date predicates.
    Checks the dates in the predicate to ensure they are in the challenge."""
    ret = {}
    ret['errors'] = []
    ret['warnings'] = []
    for action in DesignerAction.objects.filter(draft=draft):
        l = action.unlock_condition.split('unlock_on_date(')
        if len(l) > 1:
            index = l[1].find(')')
            date_string = l[1][:index].strip('"\'')
            unlock_date = datetime.strptime(date_string, "%m/%d/%y")
            if __is_after_challenge(datetime.combine(unlock_date, time(0, 0))):
                ret['errors'].append(Error(message="unlock date is after challenge end", \
                                           action=action))
            if not __is_in_rounds(datetime.combine(unlock_date, time(0, 0))):
                ret['warnings'].append(Warn(message="unlock date is not in a round", \
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


def full_designer_check(draft):
    """Runs all the designer checks (slow)."""
    ret = {}
    ret['errors'] = []
    ret['warnings'] = []
    d = check_pub_exp_dates(draft)
    for e in d['errors']:
        ret['errors'].append(e)
    for w in d['warnings']:
        ret['warnings'].append(w)
    d = check_grid_pub_exp_dates(draft)
    for e in d['errors']:
        ret['errors'].append(e)
    for w in d['warnings']:
        ret['warnings'].append(w)
    d = check_event_dates(draft)
    for e in d:
        ret['errors'].append(e)
    d = check_grid_event_dates(draft)
    for e in d:
        ret['errors'].append(e)
    d = check_designer_unlock_dates(draft)
    for e in d['errors']:
        ret['errors'].append(e)
    for w in d['warnings']:
        ret['warnings'].append(w)
    for w in check_designer_urls(draft):
        ret['warnings'].append(w)
    for e in action_dependency.check_unreachable_designer_actions(draft):
        ret['errors'].append(e)
    for w in action_dependency.check_false_unlock_designer_actions(draft):
        ret['warnings'].append(w)
    return ret


def designer_errors(draft):
    """Returns the errors detected in the Designer."""
    ret = []
    d = check_pub_exp_dates(draft)
    for e in d['errors']:
        ret.append(e)
    d = check_grid_pub_exp_dates(draft)
    for e in d['errors']:
        ret.append(e)
    for e in check_event_dates(draft):
        ret.append(e)
    for e in check_grid_event_dates(draft):
        ret.append(e)
    d = check_designer_unlock_dates(draft)
    for e in d['errors']:
        ret.append(e)
    for e in action_dependency.check_unreachable_designer_actions(draft):
        ret.append(e)
    return ret


def quick_designer_check(draft):
    """Quick test."""
    ret = {}
    ret['errors'] = []
    ret['warnings'] = []
    d = check_pub_exp_dates(draft)
    for e in d['errors']:
        ret['errors'].append(e)
    for w in d['warnings']:
        ret['warnings'].append(w)
    d = check_grid_pub_exp_dates(draft)
    for e in d['errors']:
        ret['errors'].append(e)
    for w in d['warnings']:
        ret['warnings'].append(w)
    d = check_event_dates(draft)
    for e in d:
        ret['errors'].append(e)
    d = check_grid_event_dates(draft)
    for e in d:
        ret['errors'].append(e)
    d = check_designer_unlock_dates(draft)
    for e in d['errors']:
        ret['errors'].append(e)
    for w in d['warnings']:
        ret['warnings'].append(w)
    for e in action_dependency.check_unreachable_designer_actions(draft):
        ret['errors'].append(e)
    for w in action_dependency.check_false_unlock_designer_actions(draft):
        ret['warnings'].append(w)
    return ret


def check_library_unlock_dates():
    """Checks all the LibraryAction unlock_conditions looking for unlock_on_date predicates.
    Checks the dates in the predicate to ensure they are in the challenge."""
    ret = {}
    ret['errors'] = []
    ret['warnings'] = []
    for action in LibraryAction.objects.all():
        l = action.unlock_condition.split('unlock_on_date(')
        if len(l) > 1:
            index = l[1].find(')')
            date_string = l[1][:index].strip('"\'')
            unlock_date = datetime.strptime(date_string, "%m/%d/%y")
            if not __is_in_challenge(datetime.combine(unlock_date, time(0, 0))):
                ret['errors'].append(Error(message="unlock date is not in challenge", \
                                           action=action))
            if not __is_in_rounds(datetime.combine(unlock_date, time(0, 0))):
                ret['warnings'].append(Warn(message="unlock date is not in a round", \
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


def full_library_check():
    """Runs all the consistency checks on the library returning a dictionary with the Errors and
    Warnings."""
    ret = {}
    ret['errors'] = []
    ret['warnings'] = []
    d = check_library_unlock_dates()
    for e in d['errors']:
        ret['errors'].append(e)
    for w in d['warnings']:
        ret['warnings'].append(w)
    for w in check_library_urls():
        ret['warnings'].append(w)
    for e in action_dependency.check_unreachable_library_actions():
        ret['errors'].append(e)
    for w in action_dependency.check_false_unlock_library_actions():
        ret['warnings'].append(w)
    return ret


def quick_library_check():
    """Runs the faster checks, not urls."""
    ret = {}
    ret['errors'] = []
    ret['warnings'] = []
    d = check_library_unlock_dates()
    for e in d['errors']:
        ret['errors'].append(e)
    for w in d['warnings']:
        ret['warnings'].append(w)
    for e in action_dependency.check_unreachable_library_actions():
        ret['errors'].append(e)
    for w in action_dependency.check_false_unlock_library_actions():
        ret['warnings'].append(w)
    return ret


def library_errors():
    ret = []
    d = check_library_unlock_dates()
    for e in d['errors']:
        ret.append(e)
    for e in action_dependency.check_unreachable_library_actions():
        ret.append(e)
    return ret
