# Class for node objects within tree
class Node:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []
        self.values = []
        self.parent = None
        # Pointers going both directions at bottom of tree
        self.next = None
        self.prev = None


# Class to define an object for the B+ Tree
class BPlusTree:
    def __init__(self, order=4):
        self.root = Node(is_leaf=True)
        self.order = order

    # Function that searches for a leaf node
    def leaf_search(self, rating, node):
        if node is None:
            return None

        if node.is_leaf:
            return node

        size = len(node.children)
        for i in range(size-1):
            if rating < node.keys[i]:
                return self.leaf_search(rating, node.children[i])
        return self.leaf_search(rating, node.children[-1])

    # Searches for a node with a given rating and returns the values of that node
    def search(self, rating):
        leaf = self.leaf_search(rating, self.root)
        for i in range(len(leaf.keys)):
            if leaf.keys[i] == rating:
                return leaf.values[i]
        return None

    # Function that inserts a node into the tree
    def insert(self, rating, data):
        # Find the leaf node and insert key
        leaf = self.leaf_search(rating, self.root)
        i = 0
        while i < len(leaf.keys) and leaf.keys[i] < rating:
            i += 1

        # Games with the same ratings stored in an array
        if i < len(leaf.keys) and leaf.keys[i] == rating:
            leaf.values[i].append(data)
        else:
            leaf.keys.insert(i, rating)
            leaf.values.insert(i, [data])

        # Balance the tree if there is an overflow
        curr_node = leaf
        while curr_node:
            # If there is no overflow, return
            if len(curr_node.keys) < self.order:
                return

            # Case 1: Overflow in leaf node
            if curr_node.is_leaf:
                # Split the node, where the first node has ceil((m-1) / 2) values
                new_node = Node(is_leaf=True)
                index = (self.order + 1) // 2
                new_node.keys = curr_node.keys[index:]
                new_node.values = curr_node.values[index:]
                curr_node.keys = curr_node.keys[:index]
                curr_node.values = curr_node.values[:index]

                # Assign both next and prev pointers
                new_node.next = curr_node.next
                if curr_node.next:
                    curr_node.next.prev = new_node
                curr_node.next = new_node
                new_node.prev = curr_node

            # Case 2: Overflow in non-leaf node
            else:
                # Split the node again, but the nodes should store only keys, not values
                new_node = Node()
                index = self.order // 2

                new_node.keys = curr_node.keys[index+1:]
                new_node.children = curr_node.children[index+1:]
                for child in new_node.children:
                    child.parent = new_node

                curr_node.keys = curr_node.keys[:index]
                curr_node.children = curr_node.children[:index+1]

            # Handle Parent
            if curr_node.is_leaf:
                parent_key = new_node.keys[0]
            else:
                parent_key = curr_node.keys[index]
            # If the new node will be the root for the tree
            if curr_node.parent is None:
                root = Node()
                if curr_node.is_leaf:
                    root.keys = [new_node.keys[0]]
                else:
                    root.keys = [parent_key]
                root.children = [curr_node, new_node]
                curr_node.parent = root
                new_node.parent = root
                self.root = root
                return

            # For all other nodes that aren't the root
            else:
                parent = curr_node.parent
                if curr_node.is_leaf:
                    parent_key = new_node.keys[0]

                j = 0
                while j < len(parent.children) and parent.children[j] != curr_node:
                    j += 1

                parent.keys.insert(j, parent_key)
                parent.children.insert(j+1, new_node)
                new_node.parent = parent

            curr_node = curr_node.parent

    # Helper function for merge case in delete function
    def merge(self, left, right, parent, index):
        if left.is_leaf:
            left.keys.extend(right.keys)
            left.values.extend(right.values)
            left.next = right.next
        else:
            left.keys.append(parent.keys[index])
            left.keys.extend(right.keys)
            left.children.extend(right.children)

        parent.keys.pop(index)
        parent.children.remove(right)
        self.balance_tree(parent)

    # Helper function that balances the tree after deletion
    def balance_tree(self, node):
        # If leaf node is root
        if node == self.root:
            if not node.is_leaf and len(node.children) == 1:
                self.root = node.children[0]
                self.root.parent = None
            return

        min_keys = (self.order - 1) // 2
        if len(node.keys) >= min_keys:
            return

        parent = node.parent
        index = parent.children.index(node)

        left_sibling = parent.children[index-1] if index > 0 else None
        right_sibling = parent.children[index+1] if index < len(parent.children) - 1 else None

        # Case 1: Borrow from left sibling
        if left_sibling and len(left_sibling.keys) > min_keys:
            if node.is_leaf:
                node.keys.insert(0, left_sibling.keys.pop(-1))
                node.values.insert(0, left_sibling.values.pop(-1))
                parent.keys[index-1] = node.keys[0]
            else:
                node.keys.insert(0, parent.keys[index-1])
                parent.keys[index-1] = left_sibling.keys.pop(-1)
                node.children.insert(0, left_sibling.children.pop(-1))
            return

        # Case 2: Borrow from right sibling
        if right_sibling and len(right_sibling.keys) > min_keys:
            if node.is_leaf:
                node.keys.append(right_sibling.keys.pop(0))
                node.values.append(right_sibling.values.pop(0))
                parent.keys[index] = right_sibling.keys[0]
            else:
                node.keys.append(parent.keys[index])
                parent.keys[index] = right_sibling.keys.pop(0)
                node.children.append(right_sibling.children.pop(0))
            return

        # Case 3: Merge
        if left_sibling:
            self.merge(left_sibling, node, parent, index-1)
        else:
            self.merge(node, right_sibling, parent, index)

    def delete(self, rating, data):
        leaf = self.leaf_search(rating, self.root)
        if leaf is None:
            return

        # Search for key in tree
        for i in range(len(leaf.keys)):
            if leaf.keys[i] == rating:
                # Remove value
                if data in leaf.values[i]:
                    leaf.values[i].remove(data)

                # If no values left remove key
                if len(leaf.values[i]) == 0:
                    leaf.keys.pop(i)
                    leaf.values.pop(i)

                break
        else:
            return
        self.balance_tree(leaf)

    # Find the 10 highest ratings in the tree and return an array containing tuples
    def find_highest(self, n=10):
        # Traverse down to rightmost leaf node
        curr_node = self.root
        while not curr_node.is_leaf:
            curr_node = curr_node.children[-1]
        result = []

        while curr_node and len(result) < n:
            # Backtrack through the leaf nodes right to left to get values
            for i in range(len(curr_node.keys)-1, -1, -1):
                # Also account for keys that have multiple values
                for value in curr_node.values[i]:
                    result.append((value[0], value[1], value[2], curr_node.keys[i]))
                    if len(result) >= n:
                        break
            curr_node = curr_node.prev
        return result

    # Find the 10 highest ratings in the tree given a certain filter
    def find_highest_sorted(self, n=10, genre=None, platform=None):
        if genre is None and platform is None:
            return self.find_highest()

        # Traverse down to rightmost leaf
        curr_node = self.root
        while not curr_node.is_leaf:
            curr_node = curr_node.children[-1]
        result = []

        while curr_node and len(result) < n:
            for i in range(len(curr_node.keys)-1, -1, -1):
                for value in curr_node.values[i]:
                    if genre is not None and platform is None:
                        if value[2] == genre:
                            result.append((value[0], value[1], value[2], curr_node.keys[i]))
                    elif genre is None and platform is not None:
                        if value[1] == platform:
                            result.append((value[0], value[1], value[2], curr_node.keys[i]))
                    else:
                        if value[1] == platform and value[2] == genre:
                            result.append((value[0], value[1], value[2], curr_node.keys[i]))

                    if len(result) >= n:
                        break
            curr_node = curr_node.prev
        return result
