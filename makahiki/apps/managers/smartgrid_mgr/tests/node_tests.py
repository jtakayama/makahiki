'''
Created on Mar 26, 2013

@author: makahiki
'''
import unittest
from apps.managers.smartgrid_mgr.unlock_lint import Node


class Test(unittest.TestCase):

    def setUp(self):
        self.node1 = Node("Test One", "True", "ide ntifier 1 ")

    def tearDown(self):
        pass

    def test_initialization(self):
        self.assertEqual(self.node1.name, "Test One")
        self.assertEqual(self.node1.identifier, "ide_ntifier_1")
        self.assertEqual(self.node1.expanded, True)

    def test_set_children(self):
        self.node1.update_children(" identi fier 2")
        self.assertEqual(self.node1.children, ['identi_fier_2'])

    def test_set_parent(self):
        self.node1.parent = " identi fier  1"
        self.assertEqual(self.node1.parent, 'identi_fier__1')

    def test_set_data(self):
        self.node1.data = {1: 'hello', "two": 'world'}
        self.assertEqual(self.node1.data, {1: 'hello', "two": 'world'})


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
