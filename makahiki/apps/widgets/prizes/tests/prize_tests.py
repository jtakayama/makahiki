"""Prizes test"""
import os

from django.test import TransactionTestCase
from django.conf import settings
from django.core.files.images import ImageFile
from django.db import IntegrityError

from apps.widgets.prizes.models import Prize
from django.db import transaction


class PrizeTest(TransactionTestCase):
    """
    Tests basic methods of a prize.
    """

    def testConstraints(self):
        """
        Tests that the uniqueness constraints are enforced.
        A prize with the same round_name, award_to, and competition_type as another cannot be created.
        """
        image_path = os.path.join(settings.PROJECT_ROOT, "fixtures", "test_images", "test.jpg")
        image = ImageFile(open(image_path, "r"))
        prize = Prize(
            round_name="Round 1",
            title="Super prize!",
            image=image,
            award_to="individual_overall",
            competition_type="points",
            short_description="A test prize",
            long_description="A test prize",
            value=5,
        )

        prize.save()

        prize2 = Prize(
            title="Dup prize!",
            short_description="A test prize",
            long_description="A test prize",
            image=image,
            award_to="individual_overall",
            competition_type="points",
            round_name="Round 1",
            value=5,
        )

        prize2.round_name = "Overall"
        try:
            prize2.save()
        except IntegrityError:
            self.fail("IntegrityError exception should not be thrown.")

        prize2.round_name = "Round 1"
        prize2.competition_type = "energy"
        try:
            prize2.save()
        except IntegrityError:
            self.fail("IntegrityError exception should not be thrown.")

        prize2.competition_type = "points"
        prize2.award_to = "team_overall"
        try:
            prize2.save()
        except IntegrityError:
            self.fail("IntegrityError exception should not be thrown.")

        prize2.round_name = "Round 1"
        prize2.competition_type = "points"
        prize2.award_to = "individual_overall"
        try:
            prize2.save()
            # Make sure to clean up!
            prize.image.delete()
            prize.delete()
            prize2.image.delete()
            prize2.delete()
            self.fail("IntegrityError exception not thrown.")
        except IntegrityError:
            transaction.rollback()
