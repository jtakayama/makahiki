"""Predicates regarding the state of the challenge."""

from apps.managers.challenge_mgr.models import GameInfo


def game_enabled(user, game_name):
    """Returns True if the game is enabled."""
    _ = user
    return GameInfo.objects.filter(name=game_name, enabled=True).count()


def reached_round(user, round_name):
    """Returns True."""
    return True
