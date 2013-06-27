"""handles rendering activities."""
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db import  IntegrityError
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from apps.widgets.smartgrid_play_tester.forms import TestActivityImageForm, TestActivityTextForm, \
    TestActivityFreeResponseForm, TestActivityFreeResponseImageForm
from apps.widgets.smartgrid_play_tester.models import TesterActionSubmittion


def view(request, action):
    """Returns the activity info"""

    social_email = None
    if action.member:
        social_email = action.member.social_email

    confirm_type = action.confirm_type
    if confirm_type == "image":
        form = TestActivityImageForm(
            initial={"social_email": social_email, },
            request=request)
    elif confirm_type == "text":
        question = action.pick_question(request.user.id)
        if question:
            form = TestActivityTextForm(
                initial={"question": question.pk,
                         "social_email": social_email, },
                question_id=question.pk,
                request=request)
            form.action_question = question
    elif confirm_type == "free":
        form = TestActivityFreeResponseForm(
            initial={"social_email": social_email, },
            request=request)
    elif confirm_type == "free_image":
        form = TestActivityFreeResponseImageForm(
            initial={"social_email": social_email, },
            request=request)

    form.form_title = "Get your points"

    return form


def add(request, activity):
    """Creates a request for points for an activity."""

    user = request.user
    draft = activity.draft

    if request.method == "POST":
        try:
            action_member = TesterActionSubmittion.objects.get(user=user, action=activity)
        except ObjectDoesNotExist:
            action_member = TesterActionSubmittion(user=user, action=activity, draft=draft,
                                         submission_date=datetime.datetime.today())

        action_member.approval_status = "approved"
        try:
            action_member.save()
        except IntegrityError:
            messages.error = 'Sorry, but it appears that you have already added this activity.'
            return HttpResponseRedirect(
                reverse("tester_view_action", args=(activity.type, activity.slug,)))

        response = HttpResponseRedirect(
            reverse("tester_view_action", args=(activity.type, activity.slug,)))

        return response

    return HttpResponseRedirect(reverse("tester_view_action", args=(activity.type, activity.slug,)))


def _get_form(request, activity):
    """Returns the activity form."""

    if activity.confirm_type == "image":
        form = TestActivityImageForm(request.POST, request.FILES, request=request, action=activity)
    elif activity.confirm_type == "free":
        form = TestActivityFreeResponseForm(request.POST, request=request, action=activity)
    elif activity.confirm_type == "free_image":
        form = TestActivityFreeResponseImageForm(request.POST, request.FILES, request=request,
                                             action=activity)
    else:
        form = TestActivityTextForm(request.POST, request=request, action=activity)
    return form
