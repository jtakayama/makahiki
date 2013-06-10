'''Tests the Smartgrid predicates.
Created on Jun 2, 2013

@author: Cam Moore
'''
import unittest
from django.test.testcases import TransactionTestCase
from apps.utils import test_utils
from apps.widgets.smartgrid.models import ActionMember, Level, Grid
from apps.widgets.smartgrid.predicates import submitted_action, approved_action, \
    submitted_some_of_level, approved_some_of_level, submitted_all_of_level, \
    approved_all_of_level, \
    submitted_all_of_resource, submitted_some_of_resource, approved_some_of_resource,\
    approved_all_of_resource, submitted_some_of_type, submitted_all_of_type, \
    approved_some_of_type, approved_all_of_type, submitted_some_full_spectrum,\
    approved_some_full_spectrum, submitted_some, approved_some


class PredicateTest(TransactionTestCase):
    """Tests the smartgrid predicates."""

    def setUp(self):
        """Sets up the environment for running the tests."""
        self.user = test_utils.setup_user(username="player", password="changeme")
        from apps.managers.cache_mgr import cache_mgr
        cache_mgr.clear()
        self.client.login(username="player", password="changeme")
        test_utils.set_competition_round()
        self.activity = test_utils.create_activity(slug=None, unlock_condition=None)
        self.activity.save()
        self.commitment = test_utils.create_commitment(slug=None, unlock_condition=None)
        self.commitment.save()
        self.event = test_utils.create_event(slug=None, unlock_condition=None)
        self.event.save()

    def tearDown(self):
        """Cleans up the test environment."""
        pass

    def testName(self):
        """Tests the name of the user."""
        self.assertEqual(self.user.username, "player", "Expecting player got %s" % \
                         self.user.username)

    def testAction(self):
        """Tests submitted_action and approved_action predicates."""
        self.assertFalse(submitted_some(self.user, count=1), "Haven't submitted any yet")
        action_member = ActionMember(user=self.user, action=self.activity)
        action_member.save()
        self.assertTrue(submitted_some(self.user, count=1), "Have submitted one.")
        self.assertTrue(submitted_action(self.user, self.activity.slug),
                        "submitted_action should be true")
        self.assertFalse(approved_action(self.user, self.activity.slug),
                         "approved_action should be false")
        self.assertFalse(approved_some(self.user, count=1), "Haven't had it approved yet.")
        action_member.approval_status = 'approved'
        action_member.save()
        self.assertTrue(approved_action(self.user, self.activity.slug),
                        "approved_action should be true")
        self.assertTrue(approved_some(self.user, count=1), "Have had one approved.")

    def testLevel(self):
        """Tests the level based predicates."""
        level_name = "Level Foo"
        level = Level(name=level_name, slug='level-slug', priority=1)
        level.save()
        loc = Grid(level=level, column=1, row=1, action=self.activity)
        loc.save()
        loc = Grid(level=level, column=2, row=1, action=self.commitment)
        loc.save()
        loc = Grid(level=level, column=3, row=1, action=self.event)
        loc.save()
        self.assertFalse(submitted_some_of_level(user=self.user, level_name=level_name, count=1),
                         "submitted_some_of_level should be false")
        self.assertFalse(approved_some_of_level(user=self.user, level_name=level_name, count=1),
                         "approved_some_of_level(1) should be false")
        self.assertFalse(submitted_all_of_level(user=self.user, level_name=level_name),
                         "submitted_all_of_level should be false")
        action_member_activity = ActionMember(user=self.user, action=self.activity)
        action_member_activity.save()
        self.assertTrue(submitted_some_of_level(user=self.user, level_name=level_name, count=1),
                         "submitted_some_of_level(1) should be true")
        self.assertFalse(approved_some_of_level(user=self.user, level_name=level_name, count=1),
                         "approved_some_of_level(1) should be false")
        self.assertFalse(submitted_some_of_level(user=self.user, level_name=level_name, count=2),
                         "submitted_some_of_level(2) should be false")
        self.assertFalse(submitted_all_of_level(user=self.user, level_name=level_name),
                         "submitted_all_of_level should be false")
        action_member_commitment = ActionMember(user=self.user, action=self.commitment)
        action_member_commitment.save()
        self.assertTrue(submitted_some_of_level(user=self.user, level_name=level_name, count=1),
                         "submitted_some_of_level(1) should be true")
        self.assertTrue(submitted_some_of_level(user=self.user, level_name=level_name, count=2),
                         "submitted_some_of_level(2) should be true")
        self.assertFalse(approved_some_of_level(user=self.user, level_name=level_name, count=1),
                         "approved_some_of_level(1) should be false")
        self.assertFalse(submitted_some_of_level(user=self.user, level_name=level_name, count=3),
                         "submitted_some_of_level(3) should be false")
        self.assertFalse(submitted_all_of_level(user=self.user, level_name=level_name),
                         "submitted_all_of_level should be false")
        action_member_event = ActionMember(user=self.user, action=self.event)
        action_member_event.save()
        self.assertTrue(submitted_some_of_level(user=self.user, level_name=level_name, count=1),
                         "submitted_some_of_level(1) should be true")
        self.assertTrue(submitted_some_of_level(user=self.user, level_name=level_name, count=2),
                         "submitted_some_of_level(2) should be true")
        self.assertTrue(submitted_some_of_level(user=self.user, level_name=level_name, count=3),
                         "submitted_some_of_level(3) should be true")
        self.assertTrue(submitted_all_of_level(user=self.user, level_name=level_name),
                        "submitted_all_of_level should be true")
        self.assertFalse(approved_some_of_level(user=self.user, level_name=level_name, count=1),
                         "approved_some_of_level(1) should be false")
        action_member_activity.approval_status = 'approved'
        action_member_activity.save()
        self.assertTrue(approved_some_of_level(user=self.user, level_name=level_name, count=1),
                        "approved_some_of_level(1) should be true")
        self.assertFalse(approved_all_of_level(user=self.user, level_name=level_name),
                         "approved_all_of_level should be false")
        action_member_commitment.approval_status = 'approved'
        action_member_commitment.save()
        action_member_event.approval_status = 'approved'
        action_member_event.save()
        self.assertTrue(approved_some_of_level(user=self.user, level_name=level_name, count=3),
                        "approved_some_of_level(3) should be true")
        self.assertTrue(approved_all_of_level(user=self.user, level_name=level_name),
                        "approved_all_of_level should be true")

    def testResource(self):
        """Tests the predicates related to resources."""
        self.activity.related_resource = 'water'
        self.activity.save()
        self.event.related_resource = 'energy'
        self.event.save()
        self.commitment.related_resource = 'energy'
        self.commitment.save()
        self.assertFalse(submitted_all_of_resource(self.user, resource='water'),
                         "submitted_all_of_resource should be false")
        self.assertFalse(submitted_some_of_resource(self.user, resource='water', count=1),
                         "submitted_some_of_resource should be false")
        self.assertFalse(approved_some_of_resource(self.user, resource='water', count=1),
                         "approved_some_of_resource(water) should be false")
        self.assertFalse(approved_all_of_resource(self.user, resource='water'),
                         "approved_all_of_resource(water) should be false")
        action_member_activity = ActionMember(user=self.user, action=self.activity)
        action_member_activity.save()
        self.assertTrue(submitted_some_of_resource(self.user, resource='water', count=1),
                        "submitted_some_of_resource should be true")
        self.assertTrue(submitted_all_of_resource(self.user, resource='water'),
                        "submitted_all_of_resource should be true")
        self.assertFalse(submitted_some_of_resource(self.user, resource='energy', count=1),
                         "submitted_some_of_resource(energy, 1) should be false")
        action_member_commitment = ActionMember(user=self.user, action=self.commitment)
        action_member_commitment.save()
        self.assertTrue(submitted_some_of_resource(self.user, resource='energy', count=1),
                        "submitted_some_of_resource(energy,1) should be true")
        self.assertFalse(submitted_all_of_resource(self.user, resource='energy'),
                         "submitted_all_of_resource(energy) should be false")
        action_member_event = ActionMember(user=self.user, action=self.event)
        action_member_event.save()
        self.assertTrue(submitted_some_of_resource(self.user, resource='energy', count=2),
                        "submitted_some_of_resource(energy,1) should be true")
        self.assertTrue(submitted_all_of_resource(self.user, resource='energy'),
                        "submitted_all_of_resource(energy) should be true")
        action_member_activity.approval_status = 'approved'
        action_member_activity.save()
        self.assertTrue(approved_some_of_resource(self.user, resource='water', count=1),
                         "approved_some_of_resource(water, 1) should be true")
        self.assertTrue(approved_all_of_resource(self.user, resource='water'),
                         "approved_all_of_resource(water) should be true")

    def testType(self):
        """Tests the predicates related to action_type."""
        self.assertFalse(submitted_some_of_type(self.user, action_type='activity', count=1),
                         "submitted_some_of_type(activity,1) should be false")
        self.assertFalse(submitted_some_of_type(self.user, action_type='commitment', count=1),
                         "submitted_some_of_type(commitment,1) should be false")
        self.assertFalse(submitted_some_of_type(self.user, action_type='event', count=1),
                         "submitted_some_of_type(event,1) should be false")
        self.assertFalse(submitted_all_of_type(self.user, action_type='activity'),
                         "submitted_all_of_type(activity) should be false")
        self.assertFalse(submitted_all_of_type(self.user, action_type='commitment'),
                         "submitted_all_of_type(commitment) should be false")
        self.assertFalse(submitted_all_of_type(self.user, action_type='event'),
                         "submitted_all_of_type(event) should be false")
        action_member_activity = ActionMember(user=self.user, action=self.activity)
        action_member_activity.save()
        self.assertTrue(submitted_some_of_type(self.user, action_type='activity', count=1),
                         "submitted_some_of_type(activity,1) should be true")
        self.assertFalse(submitted_some_of_type(self.user, action_type='commitment', count=1),
                         "submitted_some_of_type(commitment,1) should be false")
        self.assertFalse(submitted_some_of_type(self.user, action_type='event', count=1),
                         "submitted_some_of_type(event,1) should be false")
        self.assertTrue(submitted_all_of_type(self.user, action_type='activity'),
                         "submitted_all_of_type(activity) should be true")
        self.assertFalse(submitted_all_of_type(self.user, action_type='commitment'),
                         "submitted_all_of_type(commitment) should be false")
        self.assertFalse(submitted_all_of_type(self.user, action_type='event'),
                         "submitted_all_of_type(event) should be false")
        self.assertFalse(approved_some_of_type(self.user, action_type='activity', count=1),
                         "approved_some_of_type(activity,1) should be false")
        self.assertFalse(approved_all_of_type(self.user, action_type='activity'),
                         "approved_some_of_type(activity) should be false")
        action_member_activity.approval_status = 'approved'
        action_member_activity.save()
        self.assertTrue(approved_some_of_type(self.user, action_type='activity', count=1),
                         "approved_some_of_type(activity,1) should be true")
        self.assertTrue(approved_all_of_type(self.user, action_type='activity'),
                         "approved_some_of_type(activity) should be true")
        self.assertFalse(approved_some_of_type(self.user, action_type='event', count=1),
                         "approved_some_of_type(event,1) should be false")
        self.assertFalse(approved_all_of_type(self.user, action_type='event'),
                         "approved_some_of_type(event) should be false")

    def testFullSpectrum(self):
        """Tests the predicates related to full spectrum."""
        self.assertFalse(submitted_some_full_spectrum(self.user, count=1),
                         "submitted_some_full_spectrum(1) should be false")
        self.assertFalse(approved_some_full_spectrum(self.user, count=1),
                         "approved_some_full_spectrum(1) should be false")
        action_member_activity = ActionMember(user=self.user, action=self.activity)
        action_member_activity.save()
        self.assertFalse(submitted_some_full_spectrum(self.user, count=1),
                         "submitted_some_full_spectrum(1) should be false")
        self.assertFalse(approved_some_full_spectrum(self.user, count=1),
                         "approved_some_full_spectrum(1) should be false")
        action_member_commitment = ActionMember(user=self.user, action=self.commitment)
        action_member_commitment.save()
        action_member_event = ActionMember(user=self.user, action=self.event)
        action_member_event.save()
        self.assertTrue(submitted_some_full_spectrum(self.user, count=1),
                         "submitted_some_full_spectrum(1) should be true")
        self.assertFalse(approved_some_full_spectrum(self.user, count=1),
                         "approved_some_full_spectrum(1) should be false")
        action_member_activity.approval_status = 'approved'
        action_member_activity.save()
        self.assertFalse(approved_some_full_spectrum(self.user, count=1),
                         "approved_some_full_spectrum(1) should be false")
        action_member_commitment.approval_status = 'approved'
        action_member_commitment.save()
        action_member_event.approval_status = 'approved'
        action_member_event.save()
        self.assertTrue(approved_some_full_spectrum(self.user, count=1),
                         "approved_some_full_spectrum(1) should be true")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
