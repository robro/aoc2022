#!/usr/bin/env python
from time import perf_counter
import numpy as np

facing_offset = {
    # (y,x)
    0: np.array([0,1]),
    1: np.array([1,0]),
    2: np.array([0,-1]),
    3: np.array([-1,0])
}

def draw_path(board, path):
    facing_char = {0: '>', 1: 'v', 2: '<', 3: '^'}
    print_board = np.array(board)
    for step in path:
        print_board[tuple(step['coord'])] = facing_char[step['facing']]
    for row in print_board:
        print(''.join(row))

def get_new_facing(facing, turn):
    if turn == 'R':
        facing += 1
    elif turn == 'L':
        facing -= 1
    return facing % 4

def get_new_coord(board, coord, facing):
    test_coord = (coord + facing_offset[facing]) % board.shape
    while board[tuple(test_coord)] == ' ':
        test_coord = (test_coord + facing_offset[facing]) % board.shape
    if board[tuple(test_coord)] == '#':
        return coord
    coord = test_coord
    return coord

def main():
    with open('22/puzzle_input.txt', 'r') as f:
        input_lines = f.read().splitlines()

    width = 0
    end_index = 0
    for i, line in enumerate(input_lines):
        if not line:
            end_index = i
            break
        width = max(width, len(line))

    board = np.array([list(l.ljust(width)) for l in input_lines[:end_index]])
    instruct_string = ''.join(input_lines[end_index+1:])
    instruct_list = []
    num_str = ''
    for char in instruct_string:
        if char in ['R', 'L']:
            instruct_list.append(int(num_str))
            instruct_list.append(char)
            num_str = ''
            continue
        num_str += char
    instruct_list.append(int(num_str))

    path = []
    # Get starting state
    for x, tile in enumerate(board[0]):
        if tile == '.':
            path.append({'coord': np.array([0,x]), 'facing': 0})
            break

    cur_coord = path[0]['coord']
    facing = 0
    # Follow the instructions
    for inst in instruct_list:
        if inst in ['R', 'L']:
            facing = get_new_facing(facing, inst)
            path.append({'coord': cur_coord, 'facing': facing})
        else:
            for _ in range(inst):
                new_coord = get_new_coord(board, cur_coord, facing)
                if all(new_coord == cur_coord):
                    break
                cur_coord = new_coord
                path.append({'coord': cur_coord, 'facing': facing})
            
    final_row, final_col = path[-1]['coord']+1
    draw_path(board, path)
    print('Password:', 1000*final_row + 4*final_col + path[-1]['facing'])

if __name__ == "__main__":
    start = perf_counter()
    main()
    end = perf_counter()
    print('Completed in:', round((end - start) * 1000, 2), 'ms')
