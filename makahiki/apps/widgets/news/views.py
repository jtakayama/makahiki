import simplejson as json

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User

from managers.team_mgr.models import Post
from widgets.smartgrid import get_available_events, get_current_commitment_members, get_popular_tasks
from managers.player_mgr.models import Profile
from widgets.smartgrid.forms import EventCodeForm

def supply(request, page_name):
    team_id = request.user.get_profile().team_id

    # Get upcoming events.
    events = get_available_events(request.user)

    # Get the user's current commitments.
    commitment_members = get_current_commitment_members(request.user).select_related("commitment")

    # Get the team members.
    members = Profile.objects.filter(team=team_id).order_by(
        "-points",
        "-last_awarded_submission"
    ).select_related('user')[:12]

    form = EventCodeForm()

    return {
        "events": events,
        "commitment_members": commitment_members,
        "team_members": members,
        "popular_tasks": get_popular_tasks(),
        "event_form": form,
        }


@never_cache
@login_required
def team_members(request):
    members = User.objects.filter(profile__team=request.user.get_profile().team).order_by(
        "-profile__points",
        "-profile__last_awarded_submission",
    )

    return render_to_response("news/directory/team_members.html", {
        "team_members": members,
        }, context_instance=RequestContext(request))
