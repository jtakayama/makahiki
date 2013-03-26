'''
Created on Mar 26, 2013

@author: Cam Moore
'''
import unittest
from apps.managers.smartgrid_mgr.unlock_lint import build_trees
from apps.widgets.smartgrid_design.models import DesignerAction
from apps.widgets.smartgrid_library.models import LibraryAction


class Test(unittest.TestCase):

    def testDesignerActions(self):
        trees = build_trees(DesignerAction)
        for k in list(trees):
            t = trees[k]
            if len(t.nodes) > 1:
                t.show()
        pass

    def testLibraryActions(self):
        print "*****************************************"
        trees = build_trees(LibraryAction)
        for k in list(trees):
            t = trees[k]
            if len(t.nodes) > 1:
                t.show()
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
