"""handles rendering events."""
import urlparse

import simplejson as json

from django.db import  IntegrityError
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from apps.managers.player_mgr import player_mgr
from apps.managers.score_mgr import score_mgr

from apps.widgets.bonus_points.models import BonusPoint
import datetime
from apps.widgets.notifications.models import UserNotification
from apps.widgets.smartgrid_play_tester.forms import TestActivityCodeForm
from apps.widgets.smartgrid_play_tester.models import TesterActionSubmittion


def view(request, action):
    """Returns the activity info"""

    social_email = None
    if action.member:
        social_email = action.member.social_email

    form = TestActivityCodeForm(
            initial={"social_email": social_email, },
            request=request)

    if not action.event.is_event_completed():
        form.form_title = "Sign up for this event"
    else:
        form.form_title = "Get your points"

    return form


def add(request, event):
    """Handle the Submission and claim point of the event."""
    return signup(request, event)


def signup(request, event):
    """Commit the current user to the activity."""
    user = request.user

    action_member = TesterActionSubmittion(user=user, action=event)
    action_member.save()

    response = HttpResponseRedirect(
        reverse("activity_task", args=(event.type, event.slug,)))
    value = score_mgr.signup_points()
    notification = "You just earned " + str(value) + " points."
    response.set_cookie("task_notify", notification)
    return response
