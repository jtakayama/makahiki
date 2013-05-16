'''
Created on May 15, 2013

@author: Cam Moore
'''
import unittest
from django.test.testcases import TransactionTestCase
from apps.managers.smartgrid_mgr import grid_consistency_checker
from apps.utils import test_utils
from apps.widgets.smartgrid_design.models import DesignerEvent, DesignerAction


class Test(TransactionTestCase):
    """Tests for the Grid Consistency Checker."""
    fixtures = ['smartgrid_library.json', 'test_challenge.json', 'test_designer.json']

    def setUp(self):
        """Setup the test environment."""
        test_utils.set_three_rounds()

    def testCheckEventDates(self):
        """Tests grid_consistency_checker.check_event_dates(draft=None)"""
        errors = grid_consistency_checker.check_event_dates(draft=None)
        num_errors = len(DesignerEvent.objects.filter(draft=None)) * 2
        self.assertEqual(len(errors), num_errors, "Expecting %s errors got %s" % (num_errors, \
                                                                                  len(errors)))

    def testCheckPubDates(self):
        """Tests grid_consistency_checker.check_pub_exp_dates(draft=None)."""
        e = grid_consistency_checker.check_pub_exp_dates(draft=None)
        # one pub date is in future
        self.assertEqual(1, len(e['errors']), "Expecting %s errors got %s" % \
                         (1, len(e['errors'])))
        # all action pub dates aren't in rounds N-1 before one after.
        num_action = len(DesignerAction.objects.filter(draft=None))
        self.assertEqual(len(e['warnings']), num_action, "Expecting %s warnings got %s" % \
                         (num_action, len(e['warnings'])))

    def testCheckGridPubDates(self):
        """Tests grid_consistency_checker.check_grid_pub_exp_dates(draft=None)."""
        e = grid_consistency_checker.check_grid_pub_exp_dates(draft=None)
        num_events = len(DesignerAction.objects.filter(draft=None))
        self.assertEqual(1, len(e['errors']), "Expecting %s got %s" % (1, len(e['errors'])))
        self.assertEqual(num_events, len(e['warnings']), \
                         "Expecting %s got %s" % (num_events, len(e['warnings'])))

    def testCheckGridEventDates(self):
        """Tests grid_consistency_checker.check_grid_event_dates(draft=None)."""
        e = grid_consistency_checker.check_grid_event_dates(draft=None)
        num_events = len(DesignerEvent.objects.filter(draft=None))
        self.assertEqual(2 * num_events, len(e), "Expecting %s got %s" % (2 * num_events, len(e)))

    def testLibraryUrls(self):
        """Tests grid_consistency_checker.check_library_urls()."""
        e = grid_consistency_checker.check_library_urls()
        self.assertEqual(26, len(e), "Expecting %s got %s" % (26, len(e)))

    def testDesignerUrls(self):
        """Tests grid_consistency_checker.check_designer_urls(draft=None)."""
        e = grid_consistency_checker.check_designer_urls(draft=None)
        self.assertEqual(12, len(e), "Expecting %s got %s" % (12, len(e)))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
