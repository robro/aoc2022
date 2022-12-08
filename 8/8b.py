#!/usr/bin/env python

def getHeight(coords, tree_lines):
    # coords is a tuple of two ints: (x, y)
    x, y = coords
    return int(tree_lines[y][x])

def main():
    with open('puzzle_input.txt', 'r') as input_file:
        input_lines = input_file.read().splitlines()

    high_score = 0
    for y in range(len(input_lines)):
        for x in range(len(input_lines[0])):
            height = getHeight((x, y), input_lines)
            # look left
            vis_left = 0
            for x_left in range(x, -1, -1):
                if x_left == x:
                    continue
                vis_left += 1
                if getHeight((x_left, y), input_lines) >= height:
                    break
            # look right
            vis_right = 0
            for x_right in range(x, len(input_lines[0])):
                if x_right == x:
                    continue
                vis_right += 1
                if getHeight((x_right, y), input_lines) >= height:
                    break
            # look up
            vis_up = 0
            for y_up in range(y, -1, -1):
                if y_up == y:
                    continue
                vis_up += 1
                if getHeight((x, y_up), input_lines) >= height:
                    break
            # look down
            vis_down = 0
            for y_down in range(y, len(input_lines)):
                if y_down == y:
                    continue
                vis_down += 1
                if getHeight((x, y_down), input_lines) >= height:
                    break
            score = vis_left * vis_right * vis_up * vis_down
            if score > high_score:
                high_score = score
            
    print('Highest scenic score:', high_score)

if __name__ == "__main__":
    main()
