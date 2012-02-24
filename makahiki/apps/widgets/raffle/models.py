from django.db import models
from django.contrib.auth.models import User

from managers.settings_mgr import get_round_info

class RafflePrize(models.Model):
    ROUND_CHOICES = ((round_name, round_name) for round_name in get_round_info().keys())

    title = models.CharField(max_length=30, help_text="The title of your prize.")
    value = models.IntegerField(help_text="The value of your prize")
    description = models.TextField(
        help_text="Description of the prize.  Uses <a href='http://daringfireball.net/projects/markdown/syntax'>Markdown</a> formatting."
    )
    image = models.ImageField(
        max_length=1024,
        upload_to="prizes",
        blank=True,
        help_text="A picture of your prize."
    )
    round_name = models.CharField(
        max_length=20,
        choices=ROUND_CHOICES,
        verbose_name="Round"
    )
    winner = models.ForeignKey(User, null=True, blank=True)

    def __unicode__(self):
        return "%s: %s" % (self.deadline.round_name, self.title)

    def add_ticket(self, user):
        """
        Adds a ticket from the user if they have one.  Throws an exception if they cannot add a ticket.
        """
        profile = user.get_profile()
        if profile.available_tickets() <= 0:
            raise Exception("This user does not have any tickets to allocate.")

        ticket = RaffleTicket(raffle_prize=self, user=user)
        ticket.save()

    def remove_ticket(self, user):
        """
        Removes an allocated ticket.
        """
        # Get the first ticket that matches the query.
        ticket = RaffleTicket.objects.filter(raffle_prize=self, user=user)[0]
        ticket.delete()

    def allocated_tickets(self, user=None):
        """
        Returns the number of tickets allocated to this prize.
        Takes an optional argument to return the number of tickets allocated by the user.
        """
        query = self.raffleticket_set.filter(raffle_prize=self)
        if user:
            query = query.filter(user=user)

        return query.count()


class RaffleTicket(models.Model):
    user = models.ForeignKey(User)
    raffle_prize = models.ForeignKey(RafflePrize)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
