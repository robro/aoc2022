#!/usr/bin/env python

def getMaxBounds(lines: list[str]):
    max_x = 0
    max_y = 0
    min_x = 500
    for line in lines:
        vertices = [eval(v) for v in line.split(' -> ')]
        for vertex in vertices:
            x, y = vertex
            if x > max_x: max_x = x
            if x < min_x: min_x = x
            if y > max_y: max_y = y
    return (min_x, max_x, max_y)

def main():
    with open('puzzle_input.txt', 'r') as f:
        input_lines = f.read().splitlines()

    min_x, max_x, max_y = getMaxBounds(input_lines)
    # print(min_x, max_x, max_y)

    # generate empty cave
    cave = [['.']*((max_x - min_x)+1) for _ in range(max_y+1)]

    # use input to add features to cave
    for line in input_lines:
        vertices = [eval(v) for v in line.split(' -> ')]
        for i in range(len(vertices)):
            start_x = vertices[i][0]
            start_y = vertices[i][1]
            if i == len(vertices)-1:
                cave[start_y][start_x-min_x] = '#'
                break
            end_x = vertices[i+1][0]
            end_y = vertices[i+1][1]
            step_x = -1 if start_x > end_x else 1
            step_y = -1 if start_y > end_y else 1
            x_values = list(range(start_x, end_x, step_x))
            y_values = list(range(start_y, end_y, step_y))
            for ii in range(max(len(x_values), len(y_values))):
                x = start_x if not x_values else x_values[ii]
                y = start_y if not y_values else y_values[ii]
                cave[y][x-min_x] = '#'

    # show cave
    for row in cave:
        for tile in row:
            print(tile, end='')
        print()

if __name__ == "__main__":
    main()
