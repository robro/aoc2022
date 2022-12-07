#!/usr/bin/env python

def main():
    with open('puzzle_input.txt', 'r') as strategy_file:
        strategy_lines = strategy_file.read().splitlines()

    # win, loss, draw
    encryption = ['Z', 'X', 'Y']
    result_points = [6, 0, 3]
    matchups_me = {
        'X': 'CBA',
        'Y': 'ACB',
        'Z': 'BAC'
    }
    matchups_them = {
        'A': 'YZX',
        'B': 'ZXY',
        'C': 'XYZ'
    }
    shape_points = {
        'X': 1,
        'Y': 2,
        'Z': 3
    }

    total_score = 0
    for line in strategy_lines:
        their_shape = line[0]
        result = line[2]
        my_shape = matchups_them[their_shape][encryption.index(result)]
        total_score += (shape_points[my_shape] + 
            result_points[matchups_me[my_shape].find(their_shape)])

    print('My total score:', total_score)


if __name__ == "__main__":
    main()
