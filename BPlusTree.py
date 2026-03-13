from main import main


# Class for node objects within tree
class Node:
    def __init__(self, is_leaf=False):
        self.isLeaf = is_leaf
        self.keys = []
        self.children = []
        self.values = []
        self.next = None


# Class to define an object for the B+ Tree
class BPlusTree:
    def __init__(self, order=4):
        self.root = Node(is_leaf=True)
        self.order = order


# Function that searches for a leaf node
def leaf_search(self, rating, node):
    if node.is_leaf:
        return node

    children = node.children
    keys = node.keys
    i = 0

    size = len(children)
    for i in range(size - 1):
        if rating <= keys[i]:
            return self.leaf_search(rating, children[i])

    return self.leaf_search(rating, children[i-1])


# Searches for a node with a given rating and returns the values of that node
def search(self, rating):
    leaf = leaf_search(self, rating, self.root)
    for i in range(len(leaf.keys)):
        if leaf.keys[i] == rating:
            return leaf.values[i]
    return None
