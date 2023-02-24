from heapq import heappush, heappop
import pygame, time
import sys
from Node import Node
import numpy as np

def predefine_screen(grid):
    # initialize pygame
    pygame.init()
    # congiguration of the window
    WINDOW_SIZE = [750, 750]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # define colors of the grid RGB
    black = (0, 0, 0)  # grid == 0
    white = (255, 255, 255)  # grid == 1
    green = (50, 205, 50)  # grid == 2
    red = (255, 99, 71)  # grid == 3
    grey = (211, 211, 211)  # for background
    blue = (153, 255, 255)  # grid == 4, where current position is
    magenta = (255, 0, 255)  # grid == 5 solution

    # set the height/width of each location on the grid
    height = 6
    width = height  # i want the grid square
    margin = 1  # sets margin between grid locations

    # define goal and start
    num_rows = len(grid)
    num_columns = len(grid[0])

    idx_to_color = [black, white, green, red, blue, magenta]

    clock = pygame.time.Clock()

    return screen, grey, num_rows, num_columns, idx_to_color, margin, width, height, clock


def update_maze(screen, dic_known, grey, num_rows, num_columns, idx_to_color, margin, width, height, clock):
    screen.fill(grey)

    # dic_known 3 unfeasible 0 unknown 2 feasible
    # define start and goal
    dic_known[0, 0] = 5
    dic_known[num_rows - 1, num_columns - 1] = 5

    for row in range(num_rows):
        for column in range(num_columns):
            color = idx_to_color[dic_known[row, column]]
            pygame.draw.rect(screen, color,
                             [(margin + width) * column + margin,
                              (margin + height) * row + margin,
                              width, height])

    # set limit to 60 frames per second
    clock.tick(60)

    # update screen
    pygame.display.flip()


def forward_astar(starting_node, grid, dic_known,count):
    sys.setrecursionlimit(2500)
    # generate maze
    screen, grey, num_rows, num_columns, idx_to_color, margin, width, height, clock = predefine_screen(grid)

    # algorithm
    close_list = []
    open_list = []
    heappush(open_list, (starting_node.f_value, starting_node))
    while len(open_list) > 0:

        update_maze(screen, dic_known, grey, num_rows, num_columns, idx_to_color, margin, width, height, clock)
        current_tuple = heappop(open_list)
        current_node = current_tuple[1]
        if grid[current_node.position] == 0:
            newnode = Node(None, (current_node.parent.position))
            newnode.h_value = abs(newnode.position[0] - (len(grid) - 1)) + abs(newnode.position[1] - (len(grid) - 1))
            newnode.f_value = newnode.h_value + newnode.g_value
            dic_known[current_node.position] = 3
            # print(len(close_list))
            if len(close_list) > 0:
                count += len(close_list)
            forward_astar(newnode, grid, dic_known,count)
            break

        # if len([closed_item for closed_item in close_list if closed_item == current_node]) > 0:
        #     print(current_node.position)

        close_list.append(current_node)

        dic_known[current_node.position] = 2

        if current_node.position == (len(grid) - 1, len(grid[0]) - 1):

            count += len(close_list)
            print("reach goal")
            print(count)
            # time.sleep(10)
            break
            # print(close_list)
            # time.sleep(15)
        sucs = []
        x, y = current_node.position
        for i, j in [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]:
            if (i < 0 or j < 0 or i > len(grid) - 1 or j > len(grid[0]) - 1):
                continue

            elif (dic_known[i, j] == 3):
                continue
            node = Node(current_node, (i, j))
            sucs.append(node)
        for suc in sucs:
            if len([closed_item for closed_item in close_list if closed_item == suc]) > 0:
                continue

            suc.g_value = current_node.g_value + 1
            suc.h_value = abs(suc.position[0] - (len(grid) - 1)) + abs(suc.position[1] - (len(grid[0]) - 1))
            suc.f_value = suc.g_value + suc.h_value

            if len([open_item for open_item in open_list if
                    suc.position == open_item[1].position and suc.g_value > open_item[0]]) > 0:
                continue

            heappush(open_list, (suc.f_value, suc))

if __name__ == "__main__":
    address = "mazes_hw1/maze_1.csv"
    grid = np.genfromtxt(address, delimiter=',', dtype=int)
    dic_known = {}
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            dic_known[i,j] = 0

    # define starting node, open and close list
    start_time1 = time.time()
    starting_node1 = Node(None,(0,0))
    count1 = 0
    forward_astar(starting_node1,grid,dic_known,count1)
