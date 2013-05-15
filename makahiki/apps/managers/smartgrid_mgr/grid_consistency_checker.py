'''A checker for Draft Designer Smart Grids. Checks several different aspects of the grid and
reports Errors and Warnings.
Created on May 15, 2013

@author: Carm Moore
'''
from apps.managers.challenge_mgr import challenge_mgr
from apps.widgets.smartgrid_design.models import DesignerAction, DesignerEvent
from apps.managers.challenge_mgr.models import RoundSetting


class Error(object):
    """Represents Errors detected by GCC."""
    def __init__(self, action, message):
        """Initializer."""
        self.action = action
        self.message = message

    def __unicode__(self):
        return "Error: %s on %s" % (self.message, self.action.admin_link())

    def __str__(self):
        return "Error: %s on %s" % (self.message, self.action.admin_link())

    def __repr__(self):
        return "<Error: %s[%s]>" % (self.message, self.action.admin_link())


class Warn(object):
    """Represents Warnings detected by GCC."""
    def __init__(self, action, message):
        """Initializer."""
        self.action = action
        self.message = message

    def __unicode__(self):
        return "Warning: %s on %s" % (self.message, self.action.admin_link())

    def __str__(self):
        return "Warning: %s on %s" % (self.message, self.action.admin_link())

    def __repr__(self):
        return "<Warning: %s[%s]>" % (self.message, self.action.admin_link())


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
    return date >= challenge_mgr.get_challenge_start() and date <= challenge_mgr.get_challenge_end()


def check_pub_exp_dates(draft):
    """Returns a list of Errors for DesignerActions whose pub_date or exp_date are not in the
     challenge."""
    ret = {}
    ret['errors'] = []
    ret['warnings'] = []
    challenge_start = challenge_mgr.get_challenge_start()
    challenge_end = challenge_mgr.get_challenge_end()
    for action in DesignerAction.objects.filter(draft=draft):
        if action.pub_date > challenge_end.date():
            ret['errors'].append(Error(message="Publication Date after end of Challenge", \
                                       action=action))
        if action.expire_date and action.expire_date < challenge_start.date():
            ret['errors'].append(Error(message="Expiration date before beginning of Challenge", \
                                       action=action))
        if not __is_in_rounds(action.pub_date):
            ret['warnings'].append(Warn(message="Publication Date isn't in a round", \
                                        action=action))
        if action.expire_date and not __is_in_rounds(action.expire_date):
            ret['warnings'].append(Warn(message="Expiration Date isn't in a round", \
                                        action=action))
    return ret


def check_event_dates(draft):
    """Returns a list of Errors for DesignerEvents whose event_date isn't in the challenge or
    isn't during a round."""
    ret = []
    for event in DesignerEvent.objects.filter(draft):
        if not __is_in_rounds(event.event_date):
            ret.append(Error(message="Event date isn't in a round", action=event))
        if not __is_in_challenge(event.event_date):
            ret.append(Error(message="Event date isn't in the challenge", action=event))
    return ret
