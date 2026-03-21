# Class for node objects within tree
class Node:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
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
    def leaf_search(self, rating, node, path=None):

        if path is None:
            path = []
        path.append(node)

        if node.is_leaf:
            return node, path

        children = node.children
        keys = node.keys

        size = len(children)
        for i in range(size - 1):
            if rating < keys[i]:
                return self.leaf_search(rating, children[i], path)

        return self.leaf_search(rating, children[-1], path)

    # Searches for a node with a given rating and returns the values of that node
    def search(self, rating):
        leaf, _ = self.leaf_search(rating, self.root)
        for i in range(len(leaf.keys)):
            if leaf.keys[i] == rating:
                return leaf.values[i]
        return None

    # Function that inserts a node into the tree
    def insert(self, rating, data):
        # Use the helper function to find the node the new data will go in
        leaf, path = self.leaf_search(rating, self.root)

        # Check if the there is a duplicate rating for the game
        if rating in leaf.keys:
            index = leaf.keys.index(rating)
            if isinstance(leaf.values[index], list):
                leaf.values[index].append(data)
            else:
                leaf.values[index] = [leaf.values[index], data]

        # Otherwise, insert key normally
        else:
            i = 0
            while i < len(leaf.keys) and leaf.keys[i] < rating:
                i += 1
            leaf.keys.insert(i, rating)
            leaf.values.insert(i, [data])

        # Check if the node is now full after insertion
        k = len(leaf.keys)
        if k < self.order:
            return

        # Split leaf node
        new_leaf = Node(is_leaf=True)
        split = (k + 1) // 2

        new_leaf.keys = leaf.keys[split:]
        new_leaf.values = leaf.values[split:]
        leaf.keys = leaf.keys[:split]
        leaf.values = leaf.values[:split]

        new_leaf.next = leaf.next
        leaf.next = new_leaf

        split_key = new_leaf.keys[0]

        # Use path array to traverse up the tree
        path.pop()

        while path:
            # Copy the ceil((k+1)/2)th node to the parent
            parent = path.pop()
            index = parent.children.index(leaf)

            parent.keys.insert(index, split_key)
            parent.children.insert(index+1, new_leaf)

            if len(parent.keys) < self.order:
                return

            # Insert the new node to the parent
            internal_node = Node()
            mid = len(parent.keys) // 2
            promote = parent.keys[mid]

            internal_node.keys = parent.keys[mid+1:]
            internal_node.children = parent.children[mid+1:]
            parent.keys = parent.keys[:mid]
            parent.children = parent.children[:mid+1]

            # Continue loop until a parent is found that does not need to split
            leaf = parent
            new_leaf = internal_node
            split_key = promote

        # Split the root of the tree if needed
        new_root = Node()
        new_root.keys = [split_key]
        new_root.children = [self.root, new_leaf]
        self.root = new_root
