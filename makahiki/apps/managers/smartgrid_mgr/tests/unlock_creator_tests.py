'''Tests for the unlock_creator.
Created on Jun 3, 2013

@author: Cam Moore
'''
import unittest
from django.test.testcases import TransactionTestCase
from apps.managers.smartgrid_mgr import unlock_creator
from apps.utils import test_utils


class UnlockCreatorTest(TransactionTestCase):
    """Unlock Creator test cases."""

    def setUp(self):
        """Sets up the test environment."""
        self.activity = test_utils.create_designer_activity(slug=None, unlock_condition=None, \
                                                            draft=None)
        self.activity.save()
        test_utils.set_three_rounds()
        test_utils.enable_game(name='test game 1')
        test_utils.enable_game(name='test game 2')

    def tearDown(self):
        """Tears down the test environment."""
        pass

    def testGetChoices(self):
        """Tests the get_choices function."""
        choices = unlock_creator.get_choices('approved_action', draft=None)
        ans = len(choices)
        val = 1
        self.assertEqual(ans, val, "Expected %s action choices got %s" % (val, ans))
        choices = unlock_creator.get_choices('submitted_action', draft=None)
        ans = len(choices)
        val = 1
        self.assertEqual(ans, val, "Expected %s action choices got %s" % (val, ans))
        choices = unlock_creator.get_choices("reached_round", draft=None)
        ans = len(choices)
        val = 3
        self.assertEqual(ans, val, "Expected %s round choices got %s" % (val, ans))
        choices = unlock_creator.get_choices("game_enabled", draft=None)
        ans = len(choices)
        val = 2
        self.assertEqual(ans, val, "Expected %s game choices got %s" % (val, ans))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
