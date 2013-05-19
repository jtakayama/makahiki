'''
Created on May 15, 2013

@author: Cam Moore
'''
import unittest
from django.test.testcases import TransactionTestCase
from apps.managers.smartgrid_mgr import gcc
from apps.utils import test_utils
from apps.widgets.smartgrid_design.models import DesignerEvent, DesignerAction


class Test(TransactionTestCase):
    """Tests for the Grid Consistency Checker."""
    fixtures = ['smartgrid_library.json', 'test_challenge.json', 'test_designer.json']

    def setUp(self):
        """Setup the test environment."""
        test_utils.set_three_rounds()

    def testCheckEventDates(self):
        """Tests gcc.check_event_dates(draft=None)"""
        errors = gcc.check_event_dates(draft=None)
        num_errors = len(DesignerEvent.objects.filter(draft=None)) * 2
        self.assertEqual(len(errors), num_errors, "Expecting %s errors got %s" % (num_errors, \
                                                                                  len(errors)))

    def testCheckPubDates(self):
        """Tests gcc.check_pub_exp_dates(draft=None)."""
        e = gcc.check_pub_exp_dates(draft=None)
        # one pub date is in future
        self.assertEqual(1, len(e['errors']), "Expecting %s errors got %s" % \
                         (1, len(e['errors'])))
        # all action pub dates aren't in rounds N-1 before one after.
        num_action = len(DesignerAction.objects.filter(draft=None))
        self.assertEqual(len(e['warnings']), num_action, "Expecting %s warnings got %s" % \
                         (num_action, len(e['warnings'])))

    def testCheckGridPubDates(self):
        """Tests gcc.check_grid_pub_exp_dates(draft=None)."""
        e = gcc.check_grid_pub_exp_dates(draft=None)
        num_events = len(DesignerAction.objects.filter(draft=None))
        self.assertEqual(1, len(e['errors']), "Expecting %s got %s" % (1, len(e['errors'])))
        self.assertEqual(num_events, len(e['warnings']), \
                         "Expecting %s got %s" % (num_events, len(e['warnings'])))

    def testCheckGridEventDates(self):
        """Tests gcc.check_grid_event_dates(draft=None)."""
        e = gcc.check_grid_event_dates(draft=None)
        num_events = len(DesignerEvent.objects.filter(draft=None))
        self.assertEqual(2 * num_events, len(e), "Expecting %s got %s" % (2 * num_events, len(e)))

    # Very slow
#     def testLibraryUrls(self):
#         """Tests gcc.check_library_urls()."""
#         e = gcc.check_library_urls()
#         self.assertEqual(26, len(e), "Expecting %s got %s" % (26, len(e)))

    # Very slow
#     def testDesignerUrls(self):
#         """Tests gcc.check_designer_urls(draft=None)."""
#         e = gcc.check_designer_urls(draft=None)
#         self.assertEqual(12, len(e), "Expecting %s got %s" % (12, len(e)))

    def testLibraryUnlockDates(self):
        """Tests gcc.check_library_unlock_dates()."""
        d = gcc.check_library_unlock_dates()
        self.assertEqual(len(d['errors']), 0, "Expected 0 got %s" % len(d['errors']))
        self.assertEqual(len(d['warnings']), 0, "Expected 0 got %s" % len(d['warnings']))

    def testDesignerUnlockDates(self):
        """Tests gcc.check_designer_unlock_dates()."""
        d = gcc.check_designer_unlock_dates(draft=None)
        self.assertEqual(len(d['errors']), 1, "Expected 1 got %s" % len(d['errors']))
        self.assertEqual(len(d['warnings']), 1, "Expected 1 got %s" % len(d['warnings']))

    # Very slow
#     def testFullLibrary(self):
#         """Tests gcc.full_library_check()"""
#         d = gcc.full_library_check()
#         self.assertEqual(len(d['warnings']), 182, "Expected 182 got %s" % len(d['warnings']))
#         self.assertEqual(len(d['errors']), 0, "Expected 0 got %s" % len(d['errors']))

    def testQuickLibrary(self):
        """Tests gcc.quick_library_check()"""
        d = gcc.quick_library_check()
        print d
        self.assertEqual(len(d['warnings']), 156, "Expected 156 got %s" % len(d['warnings']))
        self.assertEqual(len(d['errors']), 0, "Expected 0 got %s" % len(d['errors']))

    def testLibraryErrors(self):
        """Tests gcc.library_errors()."""
        e = gcc.library_errors()
        self.assertEqual(len(e), 0, "Expecting 0 got %s" % len(e))

    # Very slow
#     def testFullDesigner(self):
#         """Tests gcc.full_designer_check()"""
#         d = gcc.full_designer_check(draft=None)
#         self.assertEqual(len(d['errors']), 79, "Expected 79 got %s" % len(d['errors']))
#         self.assertEqual(len(d['warnings']), 265, "Expected 265 got %s" % len(d['warnings']))

    def testQuickDesigner(self):
        """Tests gcc.quick_designer_check()"""
        d = gcc.quick_designer_check(draft=None)
        print d
        self.assertEqual(len(d['warnings']), 253, "Expected 253 got %s" % len(d['warnings']))
        self.assertEqual(len(d['errors']), 79, "Expected 79 got %s" % len(d['errors']))

    def testDesignerErrors(self):
        """Tests gcc.designer_errors(draft)."""
        d = gcc.designer_errors(draft=None)
        print d
        self.assertEqual(len(d), 79, "Expecting 79 got %s" % len(d))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
