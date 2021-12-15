import unittest
from internal_nodes import tree


class TestInternalNodes(unittest.TestCase):

    def test_count_nodes(self):
        my_tree = [4, 4, 1, 5, -1, 4, 5]
        self.assertEqual(tree.find_internal_nodes_num(my_tree), 3)

    def test_count_nodes_root(self):
        my_tree = [-1]
        self.assertEqual(tree.find_internal_nodes_num(my_tree), 1)

    def test_count_nodes_more(self):
        my_tree = [4, 4, 1, 5, -1, 4, 5, 6]
        self.assertEqual(tree.find_internal_nodes_num(my_tree), 4)

    def test_count_only_one(self):
        my_tree = [-1]
        self.assertEqual(tree.find_internal_nodes_num(my_tree), 1)

    def test_count_only_one_1_child(self):
        my_tree = [-1, 0]
        self.assertEqual(tree.find_internal_nodes_num(my_tree), 1)

    def test_count_only_more_then_two_child(self):
        my_tree = [-1, 0, 0, 0]
        self.assertEqual(tree.find_internal_nodes_num(my_tree), 1)


if __name__ == '__main__':
    unittest.main()
