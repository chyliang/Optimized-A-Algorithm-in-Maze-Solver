import argparse ,pygame, time
import numpy as np

from repeated_forward_a_star import forward_astar
from repeated_backward_a_star import backward_astar
from adaptive_a_star import adaptive_a_star
from Node import Node

import sys

if __name__ == "__main__":
    sys.setrecursionlimit(2500)

    # example: python hw1.py --maze_file=maze_0.csv
    parser = argparse.ArgumentParser()
    parser.add_argument("--maze_file", default="maze_0.csv", type=str)

    args = parser.parse_args()
    prefix = "mazes_hw1/"
    address = prefix + args.maze_file
    try:
        grid = np.genfromtxt(address, delimiter=',', dtype=int)

    except:
        raise Exception(f"Maze {address} not found.")

    dic_known = {}

    # implement forward and backward a star

    # for i in range(len(grid)):
    #     for j in range(len(grid[0])):
    #         dic_known[i,j] = 0
    #
    # # define starting node, open and close list
    # start_time1 = time.time()
    # starting_node1 = Node(None,(0,0))
    # count1 = 0
    # forward_astar(starting_node1,grid,dic_known,count1)
    # # backward_astar(starting_node,grid,dic_known)
    # print("--- %s seconds ---" % (time.time() - start_time1))
    # pygame.quit() # so that it doesnt "hang" on exit

    # implement adaptive a star

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            dic_known[i,j] = 0

    start_time2 = time.time()
    starting_node2 = Node(None,(0,0))
    dic_h_value = {}
    count2 = 0
    adaptive_a_star(starting_node2,dic_known,dic_h_value,grid,count2)
    print("--- %s seconds ---" % (time.time() - start_time2))


    pygame.quit() # so that it doesnt "hang" on exit

    exit(0)
