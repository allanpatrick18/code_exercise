# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

node = dict()
my_tree = [4, 4, 1, 5, -1, 4, 5]


def find_internal_nodes_num(tree: list) -> int:
    """
    This function will find  the num of internal nodes
    :param tree:
    :return:
    """
    if len(tree) == 1:
        return 1
    tree.remove(-1)
    size = len(set(tree))
    return size