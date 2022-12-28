import numpy as np
from numba import cuda
from math import ceil
from time import perf_counter
from colorama import init, ansi, Fore, Cursor
init()

TPB = (32, 32)

STATE_WALL = int(0b_100000)
STATE_ELF = int(0b_010000)
STATE_UP = int(0b_001000)
STATE_RIGHT = int(0b_000100)
STATE_DOWN = int(0b_000010)
STATE_LEFT = int(0b_000001)

parse_map = {
    '#': STATE_WALL,
    '^': STATE_UP,
    '>': STATE_RIGHT,
    'v': STATE_DOWN,
    '<': STATE_LEFT,
    '.': 0,
}
draw_map = {
    STATE_WALL: '#',
    STATE_ELF: 'E',
    STATE_UP: '^',
    STATE_RIGHT: '>',
    STATE_DOWN: 'v',
    STATE_LEFT: '<',
    0: '.',
}
neighbors = (
    ((-1, 0), STATE_DOWN),
    (( 0, 1), STATE_LEFT),
    (( 1, 0), STATE_UP),
    (( 0,-1), STATE_RIGHT),
)

def draw_scene(arena) -> None:
    print(Cursor.POS(1,1))
    for row in arena:
        for state in row:
            if not draw_map.get(state):
                bliz_num = 0
                for _ in range(4):
                    bliz_num += state & 1
                    state >>= 1
                print(Fore.BLUE + str(bliz_num), end='')
            elif state != STATE_ELF:
                print(Fore.BLUE + draw_map.get(state), end='')
            else:
                print(Fore.RED + 'E', end='')
        print()
    print()

@cuda.jit
def new_generation(cur_gen, new_gen, neighbors) -> None:
    y,x = cuda.grid(2)
    if (y,x) >= cur_gen.shape:
        return
    if cur_gen[y,x] == STATE_WALL:
        new_gen[y,x] = STATE_WALL
        return
    for offset, check_state in neighbors:
        check_cell = (y+offset[0], x+offset[1])
        if check_cell < (0,0):
            continue
        if check_cell >= cur_gen.shape:
            continue
        if cur_gen[check_cell] == STATE_WALL:
            check_cell = (check_cell[0]-(offset[0]*(cur_gen.shape[0]-2)),
                          check_cell[1]-(offset[1]*(cur_gen.shape[1]-2)))
            if cur_gen[check_cell] == STATE_ELF:
                continue
        new_gen[y,x] |= cur_gen[check_cell] & (check_state + STATE_ELF)

    new_gen[y,x] |= cur_gen[y,x] & STATE_ELF
    if new_gen[y,x] - STATE_ELF > 0:
        new_gen[y,x] ^= STATE_ELF

def main():
    input_lines = [line.strip('\n') for line in open('24/input.txt', 'r')]
    arena = np.array(
        [[parse_map.get(c) for c in line] for line in input_lines],
        dtype=np.int64)
    empty_arena = np.zeros(shape=arena.shape, dtype=np.int64)

    start_pos = (0, 1)
    end_pos = (arena.shape[0]-1, arena.shape[1]-2)
    arena[start_pos] = STATE_ELF

    bpg_y = ceil(arena.shape[0] / (TPB[0]))
    bpg_x = ceil(arena.shape[1] / (TPB[1]))

    for i in range(1, 300):
        new_arena = empty_arena.copy()
        new_generation[(bpg_y, bpg_x), TPB](arena, new_arena, neighbors)
        cuda.synchronize()
        if i == 1:
            print(ansi.clear_screen())
        draw_scene(new_arena)
        if new_arena[end_pos] == STATE_ELF:
            print(Fore.BLUE + 'End reached in:', Fore.RED + f'{i} minutes')
            break
        arena = new_arena

if __name__ == '__main__':
    start = perf_counter()
    main()
    end = perf_counter()
    print(Fore.BLUE + 'Completed in:', round((end - start) * 1000, 2), 'ms')