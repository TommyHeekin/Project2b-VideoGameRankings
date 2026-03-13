class Node:
    def __init__(self, isLeaf = False):
        self.isLeaf = isLeaf
        self.keys = []
        self.children = []
        self.values = []
        self.next = None

class BPlusTree:
    def __init__(self, order = 4):
        self.root = Node(isLeaf = True)
        self.order = order

