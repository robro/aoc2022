#!/usr/bin/env python

def main():
    with open('puzzle_input.txt', 'r') as strategy_file:
        strategy_lines = strategy_file.read().splitlines()

    # win, loss, tie
    result_points = [6, 0, 3]
    matchups_me = {
        'X': 'CBA',
        'Y': 'ACB',
        'Z': 'BAC'
    }
    shape_points = {
        'X': 1,
        'Y': 2,
        'Z': 3
    }

    total_score = 0
    for line in strategy_lines:
        my_shape = line[2]
        their_shape = line[0]
        total_score += (shape_points[my_shape] + 
            result_points[matchups_me[my_shape].find(their_shape)])

    print('My total score:', total_score)


if __name__ == "__main__":
    main()
