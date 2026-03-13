from bridges.bridges import *
from bridges.data_src_dependent.data_source import *
import sys
import random

def main():
    bridges = Bridges(1, "theekin", "672978654687")

    myList = get_game_data()

    game1 = myList[random.randrange(len(myList))]

    print(game1.title)
    print(game1.platform)
    print(game1.rating)
    print(game1.genre)


if __name__ == "__main__":
    main()