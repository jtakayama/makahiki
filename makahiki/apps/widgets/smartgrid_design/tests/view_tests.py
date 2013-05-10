'''
Created on May 9, 2013

@author: Cam Moore
'''
import unittest
from apps.utils import test_utils
from django.test.testcases import TransactionTestCase
from django.core.urlresolvers import reverse
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.smartgrid_mgr import smartgrid_mgr
from apps.widgets.smartgrid_design.models import DesignerColumnGrid
from django.http import Http404


class ViewTests(TransactionTestCase):
    fixtures = ['base_settings.json', 'smartgrid_library', 'test_designer.json']
    level_slug = 'level-1'
    column_slug = 'get-started'
    draft_slug = 'default'

    def setUp(self):
        """Sets up the test evironment for the Designer views."""
        self.user = test_utils.setup_superuser(username="user", password="changeme")

        challenge_mgr.register_page_widget("sgg_designer", "smartgrid_design")
#         from apps.managers.cache_mgr import cache_mgr
#         cache_mgr.clear()

        self.client.login(username="user", password="changeme")

    def testIndex(self):
        """Check that the designer page returns."""
        response = self.client.get(reverse("smartgrid_design"))
        self.failUnlessEqual(response.status_code, 200)

    def testInstantiateColumn(self):
        try:
            draft = smartgrid_mgr.get_designer_draft(self.draft_slug)
            level = smartgrid_mgr.get_designer_level(draft, self.level_slug)
            column_name = smartgrid_mgr.get_designer_column_name(draft, self.column_slug)
            response = self.client.get(reverse('instantiate_column', \
                                               args=(self.column_slug,
                                                     self.level_slug,
                                                     1,
                                                     self.draft_slug)))
            self.failUnlessEqual(response.status_code, 200)
            grid = DesignerColumnGrid.objects.filter(draft=draft, name=column_name)[0]
            self.assertIsNotNone(grid, "Didn't put %s in ColumnGrid" % self.column_slug)
            self.assertEqual(grid.column, 1, "Got column %s expecting 1" % grid.column)
            self.assertEqual(grid.level, level, "Got wrong level")
        except Http404:
            self.fail("Got 404 response")
 
#     def testInstantiateAction(self):
#         self.fail("Not implemented")
# 
#     def testMoveAction(self):
#         self.fail("Not implemented")
# 
#     def testMovePaletteAction(self):
#         self.fail("Not implemented")
# 
#     def testDeleteAction(self):
#         self.fail("Not implemented")
# 
#     def testDeleteColumn(self):
#         self.fail("Not implemented")
# 
#     def testClearFromGrid(self):
#         self.fail("Not implemented")
# 
#     def testRevertToGrid(self):
#         self.fail("Not implemented")
# 
#     def testPublishToGrid(self):
#         self.fail("Not implemented")
# 
#     def testLoadExampleGrid(self):
#         self.fail("Not implemented")
# 
#     def testRunLint(self):
#         self.fail("Not implemented")
# 
#     def testGetDiff(self):
#         self.fail("Not implemented")
# 
#     def testDeleteLevel(self):
#         self.fail("Not implemented")
# 
#     def testAddLevel(self):
#         self.fail("Not implemented")
# 
#     def testSetEventDate(self):
#         self.fail("Not implemented")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
