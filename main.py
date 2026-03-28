from bridges.bridges import *
from bridges.data_src_dependent.data_source import *
import sys
import random

from BPlusTree import *
from MaxHeap import *
from interface import *

def main():
    bridges = Bridges(1, "theekin", "672978654687")

    myList = get_game_data()
    
    bplus = BPlusTree()
    maxHeap = MaxHeap()
    for elem in myList:
        bplus.insert(elem.rating, elem)
        maxHeap.insert(elem.rating, elem)

    #choose which data structure to use right here
    app = App(bplus)
    app.mainloop()


if __name__ == "__main__":
    main()