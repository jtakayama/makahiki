'''
Created on Mar 26, 2013

@author: Cam Moore
'''
import unittest
from apps.managers.smartgrid_mgr.unlock_lint import Node, Tree
from apps.widgets.smartgrid_design.models import DesignerAction
from apps.widgets.smartgrid_library.models import LibraryAction
from apps.managers.smartgrid_mgr import unlock_lint


class Test(unittest.TestCase):

    def testDesignerActions(self):
        trees = unlock_lint.build_trees(DesignerAction)
        for k in list(trees):
            t = trees[k]
#            if len(t.nodes) > 1:
            t.show()
        pass

    def testUnreachable(self):
        slugs = unlock_lint.get_actions_not_in_trees()
        print slugs


#    def testLibraryActions(self):
#        print "*****************************************"
#        trees = build_trees(LibraryAction)
#        for k in list(trees):
#            t = trees[k]
#            if len(t.nodes) > 1:
#                t.show()
#        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
