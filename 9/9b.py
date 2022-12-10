#!/usr/bin/env python
from operator import add, sub

def main():
    with open('puzzle_input.txt', 'r') as input_file:
        input_lines = input_file.read().splitlines()

    r_pos = [(0, 0) for _ in range(10)]
    t_positions = [(0, 0)]
    move = {
        'L': (-1, 0),
        'R': (1, 0),
        'U': (0, 1),
        'D': (0, -1)
    }

    for line in input_lines:
        # move head
        for _ in range(int(line[2:])):
            r_pos[0] = tuple(map(add, r_pos[0], move[line[0]]))
            # move tail knotts
            for index in range(1, 10):
                pos_dif = list(map(sub, r_pos[index-1], r_pos[index]))
                for value in pos_dif:
                    if abs(value) > 1:
                        for i in range(2):
                            if abs(pos_dif[i]) == 2:
                                pos_dif[i] //= 2
                        r_pos[index] = tuple(map(add, pos_dif, r_pos[index]))
                        break
            t_positions.append(r_pos[9])

    print('Positions visited:', len(set(t_positions)))

if __name__ == "__main__":
    main()
