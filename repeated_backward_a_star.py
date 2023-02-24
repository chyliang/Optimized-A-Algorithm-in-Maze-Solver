from heapq import heappush, heappop
import pygame, time
import sys
from Node import Node


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

    idx_to_color = [black, white, green, red, grey, magenta]

    clock = pygame.time.Clock()

    return screen, grey, num_rows, num_columns, idx_to_color, margin, width, height, clock


def update_maze(screen, dic_know, grey, num_rows, num_columns, idx_to_color, margin, width, height, clock):

    screen.fill(grey)
    # define start and goal
    dic_know[0, 0] = 5
    dic_know[num_rows - 1, num_columns - 1] = 5

    for row in range(num_rows):
        for column in range(num_columns):
            color = idx_to_color[dic_know[row, column]]
            pygame.draw.rect(screen, color,
                             [(margin + width) * column + margin,
                              (margin + height) * row + margin,
                              width, height])

    # set limit to 60 frames per second
    clock.tick(60)

    # update screen
    pygame.display.flip()


def plan(dict_known, reversed_start, reversed_goal):
    close_list = []
    open_list = []
    heappush(open_list, (reversed_start.f_value, reversed_start))
    while len(open_list) > 0:
        current_tuple = heappop(open_list)
        current_node = current_tuple[1]
        close_list.append(current_node)
        if current_node.position == reversed_goal.position:
            return close_list
        sucs = []
        x, y = current_node.position
        for i, j in [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]:
            if (i < 0 or j < 0 or i > reversed_start.position[0] or j > reversed_start.position[1]):
                continue
            elif (dict_known[i, j] == 3):
                continue
            node = Node(current_node, (i, j))
            sucs.append(node)
        for suc in sucs:
            if len([closed_item for closed_item in close_list if closed_item == suc]) > 0:
                continue

            suc.g_value = current_node.g_value + 1
            suc.h_value = abs(suc.position[0] - reversed_goal.position[0]) + abs(
                suc.position[1] - reversed_goal.position[1])
            suc.f_value = suc.g_value + suc.h_value

            if len([open_item for open_item in open_list if
                    suc.position == open_item[1].position and suc.g_value > open_item[0]]) > 0:
                continue

            heappush(open_list, (suc.f_value, suc))


def backward_astar(starting_node, grid, dic_known):
    sys.setrecursionlimit(2500)
    # generate maze
    len_grid = len(grid)

    screen, grey, num_rows, num_columns, idx_to_color, margin, width, height, clock = predefine_screen(grid)
    count = 0
    while True:
        count +=1
        # planning
        returned_list = plan(dic_known, Node(None, (len_grid - 1, len_grid - 1)), starting_node)

        step = returned_list.pop()
        print("plan finished")

        # # show planned path
        # ptr = step
        # while ptr.position != (len_grid - 1, len_grid - 1):
        #     ptr = ptr.parent
        #     dic_known[ptr.position] = 4
        #     update_maze(screen, dic_known, grey, num_rows, num_columns, idx_to_color, margin, width, height, clock)

        # executing
        while step.position != (len_grid - 1, len_grid - 1):
            child = step
            step = step.parent
            if grid[step.position] != 0:
                dic_known[step.position] = 2
                print(step)
            else:
                starting_node = child
                dic_known[step.position] = 3
                break

        if(count%5 == 0):
            update_maze(screen, dic_known, grey, num_rows, num_columns, idx_to_color, margin, width, height, clock)
            # time.sleep(3)
        # time.sleep(2)
        if step.position == (len_grid - 1, len_grid - 1):
            print("reach goal")
            update_maze(screen, dic_known, grey, num_rows, num_columns, idx_to_color, margin, width, height, clock)
            time.sleep(60)
            break
