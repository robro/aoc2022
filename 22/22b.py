#!/usr/bin/env python
from time import perf_counter
from math import radians
import numpy as np

facing_offset = {
    # (y,x)
    0: (0,1),
    1: (1,0),
    2: (0,-1),
    3: (-1,0)
}

# Example
# edge_map = {
#     '00': (5,2),
#     '01': (3,1),
#     '02': (2,1),
#     '03': (1,1),
#     '10': (2,0),
#     '11': (4,3),
#     '12': (5,3),
#     '13': (0,1),
#     '20': (3,0),
#     '21': (4,0),
#     '22': (1,2),
#     '23': (0,0),
#     '30': (5,1),
#     '31': (4,1),
#     '32': (2,2),
#     '33': (0,3),
#     '40': (5,0),
#     '41': (1,3),
#     '42': (2,3),
#     '43': (3,3),
#     '50': (0,2),
#     '51': (1,0),
#     '52': (4,2),
#     '53': (3,2),
# }

# Puzzle input
edge_map = {
    '00': (1,0),
    '01': (2,1),
    '02': (3,0),
    '03': (5,0),
    '10': (4,2),
    '11': (2,2),
    '12': (0,2),
    '13': (5,3),
    '20': (1,3),
    '21': (4,1),
    '22': (3,1),
    '23': (0,3),
    '30': (4,0),
    '31': (5,1),
    '32': (0,0),
    '33': (2,0),
    '40': (1,2),
    '41': (5,2),
    '42': (3,2),
    '43': (2,3),
    '50': (4,3),
    '51': (1,1),
    '52': (0,1),
    '53': (3,3),
}

def draw_path(board, path, face_offsets):
    facing_char = {0: '>', 1: 'v', 2: '<', 3: '^'}
    print_board = board.copy()
    for step in path:
        print_board[tuple(step['coord'][1:]+face_offsets[step['coord'][0]])] = facing_char[step['facing']]
    for row in print_board:
        print(''.join(row))

def get_new_facing(facing, turn):
    if turn == 'R':
        facing += 1
    elif turn == 'L':
        facing -= 1
    return facing % 4

def get_new_coord(cube, coord, facing):
    new_facing = facing
    new_coord = coord.copy()
    new_coord[1:] += facing_offset[facing]
    if not ((new_coord[1:] >= 0) & (new_coord[1:] < cube.shape[1])).all():
        new_coord[0], new_facing = edge_map[str(coord[0])+str(facing)]
        new_coord[1:] = get_rotated(
            new_coord[1:], radians(((new_facing - facing)%4)*90), cube.shape[1])
    if cube[new_coord[0]][tuple(new_coord[1:])] == '#':
        return coord, facing
    return new_coord, new_facing

def get_rotated(yx, radians, length):
    y, x = yx
    y -= length/2 - 0.5
    x -= length/2 - 0.5
    c, s = np.cos(radians), np.sin(radians)
    j = np.matrix([[c, s], [-s, c]])
    m = np.dot(j, [y, x])
    coords = np.array([float(m.T[0]), float(m.T[1])]) + length/2 - 0.49 # <- dumb
    coords %= length
    return coords

def main():
    with open('22/puzzle_input.txt', 'r') as f:
        input_lines = f.read().splitlines()

    width = 0
    end_index = 0
    for y, line in enumerate(input_lines):
        if not line:
            end_index = y
            break
        width = max(width, len(line))

    board = np.array([list(l.ljust(width)) for l in input_lines[:end_index]])
    face_len = max(board.shape)//4
    face_list = []
    face_offsets = []
    for y in range(0, board.shape[0], face_len):
        for x in range(0, board.shape[1], face_len):
            face = board[y:y+face_len, x:x+face_len]
            if face[0,0] == ' ':
                continue
            face_list.append(face)
            face_offsets.append((y, x))

    cube = np.array(face_list)
    instruct_string = input_lines[end_index+1]
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
    for x, tile in enumerate(cube[0,0]):
        if tile == '.':
            path.append({'coord': np.array([0,0,x]), 'facing': 0})
            break

    cur_coord = path[0]['coord']
    facing = 0
    # Follow the instructions
    for instruction in instruct_list:
        if instruction in ['R', 'L']:
            facing = get_new_facing(facing, instruction)
            path.append({'coord': cur_coord, 'facing': facing})
            # draw_path(board, path, face_offsets)
            # input('press enter')
        else:
            for _ in range(instruction):
                new_coord, facing = get_new_coord(cube, cur_coord, facing)
                if all(new_coord == cur_coord):
                    break
                cur_coord = new_coord
                path.append({'coord': cur_coord, 'facing': facing})
                # draw_path(board, path, face_offsets)
                # input('press enter')
            
    final_face, face_row, face_col = path[-1]['coord']
    final_row = face_row + face_offsets[final_face][0]+1
    final_col = face_col + face_offsets[final_face][1]+1
    draw_path(board, path, face_offsets)
    print('Password:', 1000*final_row + 4*final_col + path[-1]['facing'])

if __name__ == "__main__":
    start = perf_counter()
    main()
    end = perf_counter()
    print('Completed in:', round((end - start) * 1000, 2), 'ms')
