from heapq import heappush, heappop
import pygame, time
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


def plan(dic_known, start, dic_h_value, grid):
    close_list = []
    open_list = []
    heappush(open_list, (start.f_value, start))
    while len(open_list) > 0:
        current_tuple = heappop(open_list)
        current_node = current_tuple[1]
        # print(current_node.position)
        close_list.append(current_node)
        if current_node.position == (len(grid) - 1, len(grid[0]) - 1):
            return close_list
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
            if suc.position not in dic_h_value:

                suc.h_value = abs(suc.position[0] - (len(grid) - 1)) + abs(
                    suc.position[1] - (len(grid[0]) - 1))
            else:
                suc.h_value = dic_h_value[suc.position]
            suc.f_value = suc.g_value + suc.h_value

            if len([open_item for open_item in open_list if
                    suc.position == open_item[1].position and suc.g_value > open_item[0]]) > 0:
                continue

            heappush(open_list, (suc.f_value, suc))


def adaptive_a_star(start, dic_known, dic_h_value, grid,count2):

    screen, grey, num_rows, num_columns, idx_to_color, margin, width, height, clock = predefine_screen(grid)

    # for i in range(len(grid)):
    #     for j in range(len(grid[0])):
    #         if dic_known[i, j] == 2:
    #             dic_known[i, j] = 0
    close_list = plan(dic_known, start, dic_h_value, grid)
    target_node = close_list[len(close_list) - 1]
    # dic_h_value = {}
    for item in close_list:
        dic_h_value[item.position] = target_node.g_value - item.g_value
    for i in range(len(close_list)):
        ptr = close_list[i]
        if grid[ptr.position] != 0:
            dic_known[ptr.position] = 2
            count2+=1
            update_maze(screen, dic_known, grey, num_rows, num_columns, idx_to_color, margin, width, height, clock)
            if ptr.position == (len(grid) - 1, len(grid[0]) - 1):
                print("reach goal")
                print(count2)
                # time.sleep(10)
                break
                # time.sleep(10)
            # print(ptr)
        else:
            dic_known[ptr.position] = 3
            update_maze(screen, dic_known, grey, num_rows, num_columns, idx_to_color, margin, width, height, clock)
            # time.sleep(3)
            adaptive_a_star(ptr.parent, dic_known, dic_h_value, grid,count2)
            break

