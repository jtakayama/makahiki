"""handles rendering events."""
from django.core.urlresolvers import reverse
from apps.managers.score_mgr import score_mgr
from apps.widgets.smartgrid_play_tester.forms import TestActivityCodeForm
from apps.widgets.smartgrid_play_tester.models import TesterActionSubmittion
from django.http import HttpResponseRedirect


def view(request, action):
    """Returns the activity info"""

    social_email = None
    if action.member:
        social_email = action.member.social_email

    form = TestActivityCodeForm(
            initial={"social_email": social_email, },
            request=request)

    if not action.is_event_completed():
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
    draft = event.draft

    action_member = TesterActionSubmittion(user=user, action=event, draft=draft)
    action_member.save()

    response = HttpResponseRedirect(
        reverse("tester_view_action", args=(event.type, event.slug,)))
    value = score_mgr.signup_points()
    notification = "You just earned " + str(value) + " points."
    response.set_cookie("task_notify", notification)
    return response
