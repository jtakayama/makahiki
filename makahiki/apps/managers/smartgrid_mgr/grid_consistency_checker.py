'''A checker for Draft Designer Smart Grids. Checks several different aspects of the grid and
reports Errors and Warnings.
Created on May 15, 2013

@author: Carm Moore
'''
from apps.managers.challenge_mgr import challenge_mgr
from apps.widgets.smartgrid_design.models import DesignerAction, DesignerEvent, DesignerGrid
from apps.managers.challenge_mgr.models import RoundSetting
import datetime
from apps.managers.smartgrid_mgr import smartgrid_mgr
import re
from apps.widgets.smartgrid_library.models import LibraryAction
import urllib2
from urllib2 import HTTPError, URLError


class Error(object):
    """Represents Errors detected by GCC."""
    def __init__(self, action, message):
        """Initializer."""
        self.action = action
        self.message = message

    def __unicode__(self):
        return "Error: %s on %s" % (self.message, self.action)

    def __str__(self):
        return "Error: %s on %s" % (self.message, self.action)

    def __repr__(self):
        return "<Error: %s[%s]>" % (self.action, self.message)

    def get_admin_link(self):
        """Returns the action's admin link."""
        return self.action.admin_link()


class Warn(object):
    """Represents Warnings detected by GCC."""
    def __init__(self, action, message):
        """Initializer."""
        self.action = action
        self.message = message

    def __unicode__(self):
        return "Warning: %s on %s" % (self.message, self.action)

    def __str__(self):
        return "Warning: %s on %s" % (self.message, self.action)

    def __repr__(self):
        return "<Warning: %s[%s]>" % (self.action, self.message)

    def get_admin_link(self):
        """Returns the action's admin link."""
        return self.action.admin_link()


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
            datetime.datetime.combine(action.expire_date, datetime.time(0, 0)) < \
            challenge_start.date():
            ret['errors'].append(Error(message="Expiration date before beginning of Challenge", \
                                       action=action))
        if not __is_in_rounds(datetime.datetime.combine(action.pub_date, datetime.time(0, 0))):
            ret['warnings'].append(Warn(message="Publication Date isn't in a round", \
                                        action=action))
        if action.expire_date and not \
            __is_in_rounds(datetime.datetime.combine(action.expire_date, datetime.time(0, 0))):
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
            datetime.datetime.combine(loc.action.expire_date, datetime.time(0, 0)) < \
            challenge_start.date():
            ret['errors'].append(Error(message="Expiration date before beginning of Challenge", \
                                       action=loc.action))
        if not __is_in_rounds(datetime.datetime.combine(loc.action.pub_date, datetime.time(0, 0))):
            ret['warnings'].append(Warn(message="Publication Date isn't in a round", \
                                        action=loc.action))
        if loc.action.expire_date and not \
            __is_in_rounds(datetime.datetime.combine(loc.action.expire_date, datetime.time(0, 0))):
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
