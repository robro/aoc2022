#!/usr/bin/env python
from operator import add

def getNeighbors(node, grid):
    x1, y1 = node
    neighbor_offsets = [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0)
    ]
    neighbors = []
    for offset in neighbor_offsets:
        x2, y2 = tuple(map(add, node, offset))
        if x2 < 0 or y2 < 0:
            continue
        if x2 >= len(grid[0]) or y2 >= len(grid):
            continue
        if ord(grid[y2][x2]) - ord(grid[y1][x1]) > 1:
            continue
        neighbors.append((x2, y2))
    return neighbors

def main():
    with open('puzzle_input.txt', 'r') as f:
        input_lines = f.read().splitlines()

    grid = [[char for char in line] for line in input_lines]

    for x in range(len(grid[0])):
        for y in range(len(grid)):
            node = (x, y)
            if grid[y][x] == 'S':
                start_node = node
                grid[y][x] = 'a'
            elif grid[y][x] == 'E':
                end_node = node
                grid[y][x] = 'z'

    queue = [start_node]
    explored = [start_node]
    parents = {}
    while len(queue) > 0:
        cur_node = queue.pop(0)
        if cur_node == end_node:
            steps = []
            while cur_node != start_node:
                steps.append(cur_node)
                cur_node = parents.pop(cur_node)
            # make a pretty picture
            for y, row in enumerate(input_lines):
                for x, marker in enumerate(row):
                    if (x, y) in steps:
                        print('.', end='')
                    else:
                        print(marker, end='')
                print()
            print()
            print('Steps:', len(steps))
            return
        for adj_node in getNeighbors(cur_node, grid):
            if adj_node not in explored:
                explored.append(adj_node)
                queue.append(adj_node)
                parents[adj_node] = cur_node

if __name__ == "__main__":
    main()
