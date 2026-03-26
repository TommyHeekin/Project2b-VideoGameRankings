# Class to define an object for the Max Heap
class MaxHeap:
    def __init__(self):
        # Each element is stored as:
        # [rating, [list of games with that rating]]
        self.heap = []
        self.index_map = {}

    # Helper function to swap two nodes
    def swap(self, i, j):
        self.index_map[self.heap[i][0]] = j
        self.index_map[self.heap[j][0]] = i
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    # Move a node up until heap property is restored
    def heapify_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[index][0] > self.heap[parent][0]:
                self.swap(index, parent)
                index = parent
            else:
                break

    # Move a node down until heap property is restored
    def heapify_down(self, index):
        size = len(self.heap)

        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            largest = index

            if left < size and self.heap[left][0] > self.heap[largest][0]:
                largest = left

            if right < size and self.heap[right][0] > self.heap[largest][0]:
                largest = right

            if largest != index:
                self.swap(index, largest)
                index = largest
            else:
                break

    # Insert a game into the heap
    def insert(self, rating, data):
        # If rating already exists, append the game to that rating bucket
        if rating in self.index_map:
            index = self.index_map[rating]
            self.heap[index][1].append(data)
            return

        # Otherwise create a new node
        self.heap.append([rating, [data]])
        index = len(self.heap) - 1
        self.index_map[rating] = index
        self.heapify_up(index)