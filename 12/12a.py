#!/usr/bin/env python
import string
from operator import add

def getNeighbors(node, heights):
    width = len(heights[0])
    height = len(heights)
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
        if x2 < 0 or y2 < 0 or x2 >= width or y2 >= height:
            continue
        if heights[y2][x2] > heights[y1][x1]+1:
            continue
        neighbors.append((x2, y2))
    return neighbors

def main():
    with open('puzzle_input.txt', 'r') as f:
        input_lines = f.read().splitlines()

    for x in range(len(input_lines[0])):
        for y in range(len(input_lines)):
            node = (x, y)
            if input_lines[y][x] == 'S':
                start_node = node
            elif input_lines[y][x] == 'E':
                end_node = node

    height_map = {k: v for v, k in enumerate(string.ascii_lowercase)}
    height_map['S'] = 0
    height_map['E'] = 25
    heights = [[height_map[char] for char in line] for line in input_lines]

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
        for adj_node in getNeighbors(cur_node, heights):
            if adj_node not in explored:
                explored.append(adj_node)
                queue.append(adj_node)
                parents[adj_node] = cur_node

if __name__ == "__main__":
    main()
