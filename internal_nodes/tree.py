

def find_internal_nodes_num(tree: list) -> int:
    """
    This function will find  the num of internal nodes
    :param tree:
    :return:
    """
    if len(tree) == 0:
        return 0
    if len(tree) == 1:
        return 1
    tree.remove(-1)
    # Time complexity is O(n)
    size = len(set(tree))
    return size

