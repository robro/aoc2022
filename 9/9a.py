#!/usr/bin/env python
from operator import add, sub

def main():
    with open('puzzle_input.txt', 'r') as input_file:
        input_lines = input_file.read().splitlines()

    h_pos = (0, 0)
    t_pos = (0, 0)
    t_positions = [t_pos]
    move = {
        'L': (-1, 0),
        'R': (1, 0),
        'U': (0, 1),
        'D': (0, -1)
    }

    for line in input_lines:
        # move head
        for _ in range(int(line[2:])):
            h_pos = tuple(map(add, h_pos, move[line[0]]))
            pos_dif = list(map(sub, h_pos, t_pos))
            # does tail need to move?
            for value in pos_dif:
                if abs(value) > 1:
                    # move tail
                    for i in range(2):
                        if abs(pos_dif[i]) == 2:
                            pos_dif[i] //= 2
                    t_pos = tuple(map(add, pos_dif, t_pos))
                    t_positions.append(t_pos)
                    break

    print('Positions visited:', len(set(t_positions)))

if __name__ == "__main__":
    main()
