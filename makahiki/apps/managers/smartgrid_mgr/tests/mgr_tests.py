'''
Created on May 4, 2013

@author: Cam Moore
'''
import unittest
from django.http import Http404
from apps.widgets.smartgrid_design.models import Draft, DesignerLevel, DesignerTextPromptQuestion, \
    DesignerAction, DesignerColumnName, DesignerColumnGrid, DesignerGrid
from django.shortcuts import get_object_or_404
from apps.managers.smartgrid_mgr import smartgrid_mgr
from apps.widgets.smartgrid_library.models import LibraryTextPromptQuestion
from apps.widgets.smartgrid.models import TextPromptQuestion, Level, ColumnName, Grid
from django.test.testcases import TransactionTestCase


class Test(TransactionTestCase):
    """Test cases for smartgrid_mgr."""
    fixtures = ['smartgrid_library', 'base_settings.json', 'test_smartgrid.json', \
                'test_designer.json']

    def __create_cams_draft(self):
        """Creates Cam's Draft smartgrid with two levels, three columns, three actions"""
        try:
            draft = get_object_or_404(Draft, slug='cam')
        except Http404:
            draft = Draft(name="Cam", slug="cam")
            draft.save()
        level1 = DesignerLevel(draft=draft, name="Foo", slug="foo", priority=1)
        level1.save()
        level2 = DesignerLevel(draft=draft, name="Bar", slug="bar", priority=2)
        level2.save()
        column1 = DesignerColumnName(draft=draft, name="Baz", slug='baz')
        column1.save()
        column2 = DesignerColumnName(draft=draft, name="Qux", slug='qux')
        column2.save()
        column3 = DesignerColumnName(draft=draft, name="Zob", slug='zob')
        column3.save()
        col_loc = DesignerColumnGrid(draft=draft, level=level1, column=5, name=column1)
        col_loc.save()
        col_loc = DesignerColumnGrid(draft=draft, level=level1, column=2, name=column2)
        col_loc.save()
        col_loc = DesignerColumnGrid(draft=draft, level=level2, column=1, name=column3)
        col_loc.save()
        action = smartgrid_mgr.instantiate_designer_action_from_library(draft, \
                                                                        'play-outside-cafe-3')
        grid_loc = DesignerGrid(draft=draft, level=level1, column=5, row=2, action=action)
        grid_loc.save()
        action = smartgrid_mgr.instantiate_designer_action_from_library(draft, \
                                                                        'use-stairs')
        grid_loc = DesignerGrid(draft=draft, level=level1, column=2, row=1, action=action)
        grid_loc.save()
        action = smartgrid_mgr.instantiate_designer_action_from_library(draft, \
                                                                        'energy-city')
        grid_loc = DesignerGrid(draft=draft, level=level2, column=5, row=5, action=action)
        grid_loc.save()

    def __clean_cams_draft(self):
        """removes Cam's draft."""
        draft = get_object_or_404(Draft, slug='cam')
        for level in DesignerLevel.objects.filter(draft=draft):
            level.delete()
        for col in DesignerColumnName.objects.filter(draft=draft):
            col.delete()
        for action in DesignerAction.objects.filter(draft=draft):
            action.delete()

    def setUp(self):
        self.__create_cams_draft()
        self.action_slug = 'intro-video'
        self.col_slug = 'get-started'
        try:
            self.draft = get_object_or_404(Draft, slug="default")
        except Http404:
            self.draft = Draft(name="Default", slug="default")
            self.draft.save()
        try:
            self.designer_level = get_object_or_404(DesignerLevel, slug='level-1')
        except Http404:
            self.designer_level = DesignerLevel(name="Level 1", slug="level-1", priority=1)
            self.designer_level.draft = self.draft
            self.designer_level.save()

    def tearDown(self):
        self.__clean_cams_draft()
        try:
            draft = get_object_or_404(Draft, slug='temp')
            draft.delete()
        except Http404:
            pass

    def testLibraryToDesigner(self):
        """Tests instantiating a DesignerAction from a LibraryAction."""
        # LibraryAction -> DesignerAction
        lib_action = smartgrid_mgr.get_library_action(self.action_slug)
        des_action = smartgrid_mgr.instantiate_designer_action_from_library(self.draft, \
                                                                            lib_action.slug)
        self.assertTrue(des_action, "Couldn't instantiate designer action %s" % lib_action.slug)
        self.assertTrue(smartgrid_mgr.get_designer_action(self.draft, self.action_slug), \
                        "Couldn't retrieve the designer action %s" % self.action_slug)
        # ensure the TextPropmptQuestions are there
        for tpq in LibraryTextPromptQuestion.objects.filter(libraryaction=lib_action):
            try:
                des_tpq = get_object_or_404(DesignerTextPromptQuestion, draft=self.draft, \
                                            question=tpq.question, answer=tpq.answer, \
                                            action=des_action)
                self.assertTrue(des_tpq, "Couldn't get DesignerTextPromptQuestion")
            except Http404:
                self.fail("Couldn't find DesignerTextPromptQuestion for %s" % tpq)
        # LibraryColumnNames -> DesignerColumnNames
        lib_column = smartgrid_mgr.get_library_column_name(self.col_slug)
        self.assertTrue(lib_column, "Couldn't get LibraryColumnName %s" % self.col_slug)
        des_column = smartgrid_mgr.instantiate_designer_column_from_library(self.draft, \
                                                                            self.col_slug)
        self.assertTrue(des_column, "Couldn't get DesignerColumnName %s" % self.col_slug)
        self.assertEqual(self.draft, des_column.draft, "Drafts are not equal.")

    def testGridToDesigner(self):
        """Tests instantiating a DesignerAction from an Action."""
        # clear the existing DesignerActions, if any.
        for des_act in DesignerAction.objects.filter(draft=self.draft, slug=self.action_slug):
            des_act.delete()
        action = smartgrid_mgr.get_smartgrid_action(self.action_slug)
        des_action = smartgrid_mgr.instantiate_designer_action_from_smartgrid(self.draft, \
                                                                              slug=action.slug)
        self.assertTrue(des_action, "Couldn't instantiate designer action %s" % action.slug)
        self.assertTrue(smartgrid_mgr.get_designer_action(self.draft, self.action_slug), \
                        "Couldn't retrieve the designer action %s" % self.action_slug)
        # ensure the TextPropmptQuestions are there
        for tpq in TextPromptQuestion.objects.filter(action=action):
            try:
                des_tpq = get_object_or_404(DesignerTextPromptQuestion, draft=self.draft, \
                                            question=tpq.question, answer=tpq.answer, \
                                            action=des_action)
                self.assertTrue(des_tpq, "Couldn't get DesignerTextPromptQuestion")
            except Http404:
                self.fail("Couldn't find DesignerTextPromptQuestion for %s" % tpq)

    def testDeploy(self):
        """Tests deploying a draft Designer Grid to the Smart Grid Game."""
        draft = get_object_or_404(Draft, slug='cam')
        smartgrid_mgr.deploy_designer_to_smartgrid(draft=draft, use_filler=False)
        # two levels
        self.assertEqual(len(Level.objects.all()), 2, "Expceting 2 levels got %s" % \
                         len(Level.objects.all()))
        self.assertTrue(Level.objects.get(slug='foo'), "Didn't get level foo")
        self.assertTrue(Level.objects.get(slug='bar'), "Didn't get level bar")
        # Three ColumnNames
        self.assertEqual(len(ColumnName.objects.all()), 3, "Expecting 3 ColumnNames got %s" % \
                         len(ColumnName.objects.all()))
        self.assertTrue(ColumnName.objects.get(slug='baz'), "Didn't get Column baz")
        self.assertTrue(ColumnName.objects.get(slug='qux'), "Didn't get Column qux")
        self.assertTrue(ColumnName.objects.get(slug='zob'), "Didn't get Column zob")
        # Three Actions in grid
        self.assertEqual(len(Grid.objects.all()), 3, "Expecting 3 actions in grid got %s" % \
                         len(Grid.objects.all()))

    def testRevert(self):
        """Tests reverting to the current Smartgrid."""
        try:
            draft = get_object_or_404(Draft, slug='temp')
        except Http404:
            draft = Draft(name='Temp', slug='temp')
            draft.save()
        smartgrid_mgr.copy_smartgrid_to_designer(draft)
        self.assertEqual(len(DesignerLevel.objects.filter(draft=draft)), 4, \
                         "Expecting 4 levels got %s" % \
                         len(DesignerLevel.objects.filter(draft=draft)))
        self.assertEqual(len(DesignerColumnName.objects.filter(draft=draft)), 30, \
                         "Expecting 30 ColumnNames got %s" % \
                         len(DesignerColumnName.objects.filter(draft=draft)))
        self.assertEqual(len(DesignerAction.objects.filter(draft=draft)), 84, \
                         "Expecting 84 Actions got %s" % \
                         len(DesignerAction.objects.filter(draft=draft)))

    def testLoadExampleGrid(self):
        """Tests load_example_grid(draft, example_name)."""
        try:
            draft = get_object_or_404(Draft, slug='temp2')
        except Http404:
            draft = Draft(name='Temp', slug='temp2')
            draft.save()
        smartgrid_mgr.load_example_grid(draft, 'test')
        self.assertEqual(len(DesignerLevel.objects.filter(draft=draft)), 4, \
                         "Expecting 4 levels got %s" % \
                         len(DesignerLevel.objects.filter(draft=draft)))
        self.assertEqual(len(DesignerColumnName.objects.filter(draft=draft)), 30, \
                         "Expecting 30 ColumnNames got %s" % \
                         len(DesignerColumnName.objects.filter(draft=draft)))
        self.assertEqual(len(DesignerAction.objects.filter(draft=draft)), 84, \
                         "Expecting 84 Actions got %s" % \
                         len(DesignerAction.objects.filter(draft=draft)))
        val = len(DesignerGrid.objects.filter(draft=draft))
        ans = 84
        self.assertEqual(val, ans, "Expecting %s got %s" % (ans, val))
        try:
            draft = get_object_or_404(Draft, slug='temp3')
        except Http404:
            draft = Draft(name='Temp3', slug='temp3')
            draft.save()
        smartgrid_mgr.load_example_grid(draft, 'demo')
        val = len(DesignerLevel.objects.filter(draft=draft))
        ans = 3
        self.assertEqual(val, ans, "Expecting %s got %s" % (ans, val))
        val = len(DesignerColumnName.objects.filter(draft=draft))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
