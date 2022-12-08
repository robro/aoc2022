#!/usr/bin/env python

def main():
    with open('puzzle_input.txt', 'r') as input_file:
        input_lines = input_file.read().splitlines()

    visible_trees = []
    # coordinates are a tuple of two ints (x, y)
    
    # check from left
    for y, row in enumerate(input_lines):
        tallest_tree = -1
        for x, height in enumerate(row):
            if int(height) > tallest_tree:
                tallest_tree = int(height)
                visible_trees.append((x, y))

    # check from right
    for y, row in enumerate(input_lines):
        tallest_tree = -1
        for x, height in enumerate(reversed(row)):
            if int(height) > tallest_tree:
                tallest_tree = int(height)
                visible_trees.append(((len(row)-1)-x, y))

    # check from top
    for x in range(len(input_lines[0])):
        tallest_tree = -1
        for y in range(len(input_lines)):
            height = int(input_lines[y][x])
            if height > tallest_tree:
                tallest_tree = height
                visible_trees.append((x, y))

    # check from bottom
    for x in range(len(input_lines[0])):
        tallest_tree = -1
        for y in reversed(range(len(input_lines))):
            height = int(input_lines[y][x])
            if height > tallest_tree:
                tallest_tree = height
                visible_trees.append((x, y))

    print('Visible trees:', len(set(visible_trees)))

if __name__ == "__main__":
    main()
