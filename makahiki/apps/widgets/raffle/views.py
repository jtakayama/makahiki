import datetime
from django.conf import settings

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.views.decorators.cache import never_cache

from managers.settings_mgr import  get_current_round, get_current_round_info
from widgets.raffle.models import  RafflePrize


POINTS_PER_TICKET = 25      # Number of points for each raffle ticket.
RAFFLE_END_PERIOD = 2       # raffle end 2 hours before round ends

def supply(request, page_name):
    user = request.user
    current_round_info = get_current_round_info()
    deadline  = current_round_info["end"] - datetime.timedelta(hours=RAFFLE_END_PERIOD)
    today = datetime.datetime.today()

    # Get the user's tickets.
    profile = user.get_profile()
    available_tickets = profile.available_tickets()
    total_tickets = profile.points / POINTS_PER_TICKET
    allocated_tickets = total_tickets - available_tickets

    prizes = None
    if today < deadline:
        # Get the prizes for the raffle.
        prizes = RafflePrize.objects.filter(round_name=current_round_info["name"]).order_by("-value")

    return {
        "round_name": current_round_info["name"],
        "deadline": deadline,
        "today": today,
        "points_per_ticket": POINTS_PER_TICKET,
        "tickets": {
            "available": available_tickets,
            "total": total_tickets,
            "allocated": allocated_tickets,
            },
        "prizes": prizes,
        }


@login_required
def add_ticket(request, prize_id):
    """
    Adds a user's raffle ticket to the prize.
    """
    if request.method == "POST":
        prize = get_object_or_404(RafflePrize, id=prize_id)
        profile = request.user.get_profile()
        current_round_info = get_current_round_info()
        deadline  = current_round_info["end"] - datetime.timedelta(hours=RAFFLE_END_PERIOD)
        in_deadline = datetime.datetime.today() <= deadline

        #print profile.available_tickets()
        if profile.available_tickets() > 0 and in_deadline:
            prize.add_ticket(request.user)
            return HttpResponseRedirect(reverse("prizes_index"))
        elif not in_deadline:
            messages.error(request, "The raffle for this round is over.")
            return HttpResponseRedirect(reverse("prizes_index"))
        else:
            messages.error(request, "Sorry, but you do not have any more tickets.")
            return HttpResponseRedirect(reverse("prizes_index"))

    raise Http404


@login_required
def remove_ticket(request, prize_id):
    """
    Removes a user's raffle ticket from the prize.
    """
    if request.method == "POST":
        prize = get_object_or_404(RafflePrize, id=prize_id)
        if prize.allocated_tickets(request.user) > 0:
            prize.remove_ticket(request.user)
            return HttpResponseRedirect(reverse("prizes_index"))

        else:
            messages.error(request, "Sorry, but you do not have any tickets for this prize.")
            return HttpResponseRedirect(reverse("prizes_index"))

    raise Http404


@never_cache
@user_passes_test(lambda u: u.is_staff, login_url="/account/cas/login")
def raffle_form(request, prize_id):
    _ = request
    prize = get_object_or_404(RafflePrize, pk=prize_id)
    return render_to_response('view_prizes/form.txt', {
        'raffle': True,
        'prize': prize,
        'round': prize.deadline.round_name
    }, mimetype='text/plain')