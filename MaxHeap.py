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

        # if not, create a new node
        self.heap.append([rating, [data]])
        index = len(self.heap) - 1
        self.index_map[rating] = index
        self.heapify_up(index)

   # Search for all games with a certain rating
    def search(self, rating):
        games = []
        for ratings, values in self.heap:
            if ratings >= rating:
                games.extend(values)
       
       # games.sort(reverse=True, key=lambda x:x[2])
        return (games)

    # Delete one specific game from a rating bucket
    def delete(self, rating, data):
        if rating not in self.index_map:
            return

        index = self.index_map[rating]
        values = self.heap[index][1]

        if data not in values:
            return

        # Remove the specific game
        values.remove(data)

        # If there are still games with that rating, stop here
        if len(values) > 0:
            return

        # Otherwise remove the whole node
        last_index = len(self.heap) - 1
        del self.index_map[rating]

        # If it is already the last node, just pop it
        if index == last_index:
            self.heap.pop()
            return

        # Move the last node into this spot
        self.heap[index] = self.heap[last_index]
        moved_rating = self.heap[index][0]
        self.index_map[moved_rating] = index
        self.heap.pop()

        # Restore heap property
        if index > 0 and self.heap[index][0] > self.heap[(index - 1) // 2][0]:
            self.heapify_up(index)
        else:
            self.heapify_down(index)

    # Return the highest-rated node without removing it
    def peek_max(self):
        if len(self.heap) == 0:
            return None
        return self.heap[0]

    # Remove an entire rating node
    def remove_max_node(self):
        if len(self.heap) == 0:
            return None

        max_node = self.heap[0]
        last_index = len(self.heap) - 1
        del self.index_map[max_node[0]]

        if last_index == 0:
            self.heap.pop()
            return max_node

        self.heap[0] = self.heap[last_index]
        self.index_map[self.heap[0][0]] = 0
        self.heap.pop()
        self.heapify_down(0)

        return max_node

    # Find the n highest-rated games
    def find_highest(self, n=10):
        result = []

        # Copy heap manually so original is unchanged
        temp = MaxHeap()
        for rating, values in self.heap:
            temp.heap.append([rating, values.copy()])
        temp.index_map = self.index_map.copy()

        while len(temp.heap) > 0 and len(result) < n:
            max_node = temp.remove_max_node()
            rating = max_node[0]
            games = max_node[1]

            for game in games:
                result.append((game[0], game[1], game[2], rating))
                if len(result) >= n:
                    break

        return result

    # Find the n highest-rated games with filters
    def find_highest_sorted(self, n=10, genre=None, platform=None):
        if genre is None and platform is None:
            return self.find_highest(n)

        result = []

        temp = MaxHeap()
        for rating, values in self.heap:
            temp.heap.append([rating, values.copy()])
        temp.index_map = self.index_map.copy()

        while len(temp.heap) > 0 and len(result) < n:
            max_node = temp.remove_max_node()
            rating = max_node[0]
            games = max_node[1]

            for game in games:
                if genre is not None and platform is None:
                    if game[2] == genre:
                        result.append((game[0], game[1], game[2], rating))
                elif genre is None and platform is not None:
                    if game[1] == platform:
                        result.append((game[0], game[1], game[2], rating))
                else:
                    if game[1] == platform and game[2] == genre:
                        result.append((game[0], game[1], game[2], rating))

                if len(result) >= n:
                    break

        return result