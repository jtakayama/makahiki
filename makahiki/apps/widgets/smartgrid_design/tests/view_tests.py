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
from apps.widgets.smartgrid_design.models import DesignerColumnGrid, DesignerLevel, Draft, \
    DesignerGrid
from django.http import Http404
from apps.widgets.smartgrid.models import Level, Activity, ColumnName, ColumnGrid, Grid


class ViewTests(TransactionTestCase):
    """Tests for smartgrid_design/views.py."""
    fixtures = ['base_settings.json', 'smartgrid_library', ]
    draft_slug = 'default'
    level_slug = 'level-1'
    column_slug = 'get-started'
    action_slug = 'room-energy'

    def setUp(self):
        """Sets up the test evironment for the Designer views."""
        self.user = test_utils.setup_superuser(username="user", password="changeme")

        challenge_mgr.register_page_widget("sgg_designer", "smartgrid_design")
        from apps.managers.cache_mgr import cache_mgr
        cache_mgr.clear()

        self.client.login(username="user", password="changeme")
        try:
            draft = smartgrid_mgr.get_designer_draft(self.draft_slug)
        except Http404:  # shouldn't happen Default draft is defined in base_settings
            draft = Draft(name='Default', slug='default')
            draft.save()
        try:
            level = smartgrid_mgr.get_designer_level(draft, self.level_slug)
        except Http404:  # ensure there is a DesignerLevel
            level = DesignerLevel(name="Level 1", slug=self.level_slug, priority=1, draft=draft)
            level.save()

    def testIndex(self):
        """Check that the designer page returns."""
        response = self.client.get(reverse("smartgrid_design"))
        self.failUnlessEqual(response.status_code, 200)

    def testInstantiateColumn(self):
        """Test instantiating DesignerColumnName from LibraryColumnName using the url interface."""
        response = self.client.get(reverse('instantiate_column', \
                                           args=(self.column_slug,
                                                 self.level_slug,
                                                 1,
                                                 self.draft_slug)))
        self.failUnlessEqual(response.status_code, 200)
        try:
            draft = smartgrid_mgr.get_designer_draft(self.draft_slug)
            level = smartgrid_mgr.get_designer_level(draft, self.level_slug)
            column_name = smartgrid_mgr.get_designer_column_name(draft, self.column_slug)
            qs = DesignerColumnGrid.objects.filter(draft=draft, name=column_name)
            self.assertEquals(len(qs), 1, "Got the wrong number of Columns expecting 1 got %s" % \
                              len(qs))
            grid = qs[0]
            self.assertIsNotNone(grid, "Didn't put %s in ColumnGrid" % self.column_slug)
            self.assertEqual(grid.column, 1, "Got column %s expecting 1" % grid.column)
            self.assertEqual(grid.level, level, "Got wrong level")
        except Http404:
            self.fail("Got 404 response, designer objects didn't instantiate")

    def testInstantiateAction(self):
        """Test instantiating DesignerAction from LibraryAction using the url interface."""
        response = self.client.get(reverse('instantiate_action', \
                                           args=(self.action_slug,
                                                 self.level_slug,
                                                 2,
                                                 2,
                                                 self.draft_slug)))
        self.failUnlessEqual(response.status_code, 200)
        try:
            draft = smartgrid_mgr.get_designer_draft(self.draft_slug)
            level = smartgrid_mgr.get_designer_level(draft, self.level_slug)
            action = smartgrid_mgr.get_designer_action(draft, self.action_slug)
            qs = DesignerGrid.objects.filter(draft=draft, action=action)
            self.assertEquals(len(qs), 1, "Got the wrong number of Actions expecting 1 got %s" % \
                              len(qs))
            loc = qs[0]
            self.assertIsNotNone(loc, "Didn't put the DesignerAction in the grid")
            self.assertEqual(loc.column, 2, "Got column %s expecting 2" % loc.column)
            self.assertEqual(loc.row, 2, "Got row %s expecting 2" % loc.row)
            self.assertEqual(loc.level, level, "Got wrong level")
        except Http404:
            self.fail("Got 404 response, designer objects didn't instantiate")

    def testMoveAction(self):
        """Tests moving a DesignerAction in the Grid using the url interface."""
        # Setup the action to move, ensure it is in the right place.
        draft = smartgrid_mgr.get_designer_draft(self.draft_slug)
        level = smartgrid_mgr.get_designer_level(draft, self.level_slug)
        self.client.get(reverse('instantiate_action', \
                                args=(self.action_slug,
                                      self.level_slug,
                                      2,
                                      2,
                                      self.draft_slug)))
        response = self.client.get(reverse('move_action', \
                                           args=(self.action_slug,
                                                 self.level_slug,
                                                 2,
                                                 2,
                                                 3,
                                                 1,
                                                 self.draft_slug)))
        self.failUnlessEqual(response.status_code, 200)
        action = smartgrid_mgr.get_designer_action(draft, self.action_slug)
        qs = DesignerGrid.objects.filter(draft=draft, action=action)
        self.assertEquals(len(qs), 1, "Got the wrong number of Actions expecting 1 got %s" % \
                          len(qs))
        loc = qs[0]
        self.assertIsNotNone(loc, "Didn't put the DesignerAction in the grid")
        self.assertEqual(loc.column, 3, "Got column %s expecting 3" % loc.column)
        self.assertEqual(loc.row, 1, "Got row %s expecting 1" % loc.row)
        self.assertEqual(loc.level, level, "Got wrong level")

    def testMovePaletteAction(self):
        """Tests moving a DesignerAction from the Palette to the DesignerGrid using the url
        interface."""
        # Setup the action to move, ensure it is in the right place.
        self.client.get(reverse('instantiate_action', \
                                args=(self.action_slug,
                                      self.level_slug,
                                      2,
                                      2,
                                      self.draft_slug)))
        draft = smartgrid_mgr.get_designer_draft(self.draft_slug)
        action = smartgrid_mgr.get_designer_action(draft, self.action_slug)
        qs = DesignerGrid.objects.filter(action=action)
        for loc in qs:
            loc.delete()  # moves the action into the palette
        response = self.client.get(reverse('move_palette_action', \
                                           args=(self.action_slug,
                                                 self.level_slug,
                                                 5,
                                                 2,
                                                 self.draft_slug)))
        self.failUnlessEqual(response.status_code, 200)
        qs = DesignerGrid.objects.filter(action=action)
        self.assertEquals(len(qs), 1, "Got the wrong number of Actions expecting 1 got %s" % \
                          len(qs))
        loc = qs[0]
        self.assertIsNotNone(loc, "Didn't put the DesignerAction in the grid")
        self.assertEqual(loc.column, 5, "Got column %s expecting 5" % loc.column)
        self.assertEqual(loc.row, 2, "Got row %s expecting 2" % loc.row)
        level = smartgrid_mgr.get_designer_level(draft, self.level_slug)
        self.assertEqual(loc.level, level, "Got wrong level")

    def testDeleteAction(self):
        """Tests deleting a DesignerAction using the url interface."""
        # Setup the action to delete, ensure it is in the right place.
        self.client.get(reverse('instantiate_action', \
                                args=(self.action_slug,
                                      self.level_slug,
                                      2,
                                      2,
                                      self.draft_slug)))
        response = self.client.get(reverse('delete_designer_action', \
                                           args=(self.action_slug,
                                                 self.draft_slug)))
        self.failUnlessEqual(response.status_code, 200)
        draft = smartgrid_mgr.get_designer_draft(self.draft_slug)
        try:
            smartgrid_mgr.get_designer_action(draft, self.action_slug)
            self.fail("Didn't delete DesignerAction %s" % self.action_slug)
        except Http404:
            pass

    def testDeleteColumn(self):
        """Tests deleting a DesignerColumnName using the url interface."""
        # Setup the column to delete
        self.client.get(reverse('instantiate_column', \
                                args=(self.column_slug,
                                      self.level_slug,
                                      1,
                                      self.draft_slug)))
        response = self.client.get(reverse('delete_designer_column', \
                                   args=(self.column_slug,
                                         self.draft_slug)))
        self.failUnlessEqual(response.status_code, 200)
        draft = smartgrid_mgr.get_designer_draft(self.draft_slug)
        try:
            smartgrid_mgr.get_designer_column_name(draft, self.column_slug)
            self.fail("Didn't delete DesignerColumnName %s" % self.column_slug)
        except Http404:
            pass

    def testClearFromGrid(self):
        """Test removing a DesignerAction from the DesignerGrid using the url interface."""
        # Setup the action to move to the palette, ensure it is in the right place.
        self.client.get(reverse('instantiate_action', \
                                args=(self.action_slug,
                                      self.level_slug,
                                      2,
                                      2,
                                      self.draft_slug)))
        response = self.client.get(reverse('clear_from_grid', \
                                           args=(self.action_slug,
                                                 self.draft_slug)))
        self.failUnlessEqual(response.status_code, 200)
        draft = smartgrid_mgr.get_designer_draft(self.draft_slug)
        action = smartgrid_mgr.get_designer_action(draft, self.action_slug)
        qs = DesignerGrid.objects.filter(action=action)
        self.failUnlessEqual(len(qs), 0, "Didn't remove the DesignerAction from the grid.")

    def testRevertToGrid(self):
        """Tests reverting the DesignerGrid to the SmartGrid using the url interface."""
        # set up really fake designer grid
        self.client.get(reverse('instantiate_action', \
                                args=(self.action_slug,
                                      self.level_slug,
                                      2,
                                      2,
                                      self.draft_slug)))
        # set up fake smartgrid
        level = Level(name='Foo', slug='foo', priority=1)
        level.save()
        action = Activity(name='Test', slug='test', title='test title', description='description', \
                          type='activity', expected_duration=2)
        action.save()
        column = ColumnName(name='Column', slug='column')
        column.save()
        loc = ColumnGrid(level=level, column=1, name=column)
        loc.save()
        loc = Grid(level=level, column=1, row=2, action=action)
        loc.save()
        response = self.client.post(reverse('revert_to_grid', args=(self.draft_slug, )), {}, \
                                    follow=True)
        self.failUnlessEqual(response.status_code, 200)
        draft = smartgrid_mgr.get_designer_draft(self.draft_slug)
        try:
            smartgrid_mgr.get_designer_action(draft, self.action_slug)
            self.fail("Old Action should be deleted")
        except Http404:
            pass
        try:
            level = smartgrid_mgr.get_designer_level(draft, slug='foo')
        except Http404:
            self.fail("Didn't copy Level Foo to designer.")
        try:
            action = smartgrid_mgr.get_designer_action(draft, slug='test')
        except Http404:
            self.fail("Didn't copy action Test to designer.")
        try:
            column = smartgrid_mgr.get_designer_column_name(draft, slug='column')
        except Http404:
            self.fail("Didn't copy the ColumnName to designer.")
        qs = DesignerColumnGrid.objects.filter(name=column)
        self.failUnlessEqual(len(qs), 1, "Column is not in Designer Grid")
        loc = qs[0]
        self.failUnlessEqual(loc.level, level, "Wrong level in Designer Grid")
        self.failUnlessEqual(loc.column, 1, "Wrong column in Designer Grid")
        self.failUnlessEqual(loc.name, column, "Wrong column name in Designer Grid")
        qs = DesignerGrid.objects.filter(action=action)
        self.failUnlessEqual(len(qs), 1, "Action is not in Designer Grid")
        loc = qs[0]
        self.failUnlessEqual(loc.level, level, "Wrong level in Designer Grid")
        self.failUnlessEqual(loc.column, 1, "Wrong column in Designer Grid")
        self.failUnlessEqual(loc.row, 2, "Wrong row in Designer Grid")

    def testPublishToGrid(self):
        """Tests publishing a DesignerGrid to the SmartGrid."""
        # set up really fake designer grid
        self.client.get(reverse('instantiate_action', \
                                args=(self.action_slug,
                                      self.level_slug,
                                      2,
                                      2,
                                      self.draft_slug)))
        self.client.get(reverse('instantiate_column', \
                                args=(self.column_slug,
                                      self.level_slug,
                                      2,
                                      self.draft_slug)))
        response = self.client.post(reverse('publish_to_grid', args=(self.draft_slug, )), \
                                    {}, follow=True)
        self.failUnlessEqual(response.status_code, 200)
        try:
            level = smartgrid_mgr.get_smartgrid_level(slug=self.level_slug)
        except Http404:
            self.fail("Didn't copy level to smartgrid")
        try:
            column = smartgrid_mgr.get_smartgrid_column_name(slug=self.column_slug)
        except Http404:
            self.fail("Didn't copy ColumnName to smartgrid")
        try:
            action = smartgrid_mgr.get_smartgrid_action(slug=self.action_slug)
        except Http404:
            self.fail("Didn't copy Action to smartgrid")
        qs = ColumnGrid.objects.filter(name=column)
        self.failUnlessEqual(len(qs), 1, "Didn't put column in the grid")
        loc = qs[0]
        self.failUnlessEqual(loc.level, level, "Wrong level for column name")
        self.failUnlessEqual(loc.column, 2, "Wrong column for column name")
        qs = Grid.objects.filter(action=action)
        self.failUnlessEqual(len(qs), 1, "Didn't put action in the grid")
        loc = qs[0]
        self.failUnlessEqual(loc.level, level, "Wrong level for action")
        self.failUnlessEqual(loc.column, 2, "Wrong column for action")
        self.failUnlessEqual(loc.row, 2, "Wrong row for action")

#     def testLoadExampleGrid(self):
#         self.fail("Not implemented")

#     def testRunLint(self):
#         self.fail("Not implemented")

#     def testGetDiff(self):
#         self.fail("Not implemented")

#     def testDeleteLevel(self):
#         self.fail("Not implemented")

#     def testAddLevel(self):
#         self.fail("Not implemented")

#     def testSetEventDate(self):
#         self.fail("Not implemented")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
