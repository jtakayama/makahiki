'''
Created on Mar 26, 2013

@author: makahiki
'''
import unittest
from apps.managers.smartgrid_mgr.unlock_lint import Tree

(_ADD, _DELETE, _INSERT) = range(3)
(_ROOT, _DEPTH, _WIDTH) = range(3)


class TestTree(unittest.TestCase):
    def setUp(self):
        pass

    def test_initialization(self):
        tree = Tree()
        tree.create_node("Harry", "True", "harry")  # root node
        tree.create_node("Jane", "True", "jane", parent="harry")
        tree.create_node("Bill", "True", "bill", parent="harry")
        tree.create_node("Diane", "True", "diane", parent="jane")
        tree.create_node("George", "True", "george", parent="diane")
        tree.create_node("Mary", "True", "mary", parent="diane")
        tree.create_node("Jill", "True", "jill", parent="george")
        tree.create_node("Mark", "True", "mark", parent="jane")
        tree.show()
        print("=" * 80)
        for node in tree.expand_tree(mode=_DEPTH):
            print tree[node].name
        pass

    def tearDown(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']

    unittest.main()
