#!/usr/bin/env python
import os
import numpy as np
from time import perf_counter

STATE_ELF = 16
STATE_UP = 8
STATE_RIGHT = 4
STATE_DOWN = 2
STATE_LEFT = 1

parse_map = {
    '^': STATE_UP,
    '>': STATE_RIGHT,
    'v': STATE_DOWN,
    '<': STATE_LEFT,
    '.': 0,
}
draw_map = {
    STATE_ELF: 'E',
    STATE_UP: '^',
    STATE_RIGHT: '>',
    STATE_DOWN: 'v',
    STATE_LEFT: '<',
    0: '.',
}
neighbors = {
    ( 0,-1): STATE_DOWN,
    ( 1, 0): STATE_LEFT,
    ( 0, 1): STATE_UP,
    (-1, 0): STATE_RIGHT,
}

def draw_scene(generation: dict, dimensions) -> None:
    width, height = dimensions
    for y in range(height):
        for x in range(width):
            state = generation.get((x, y))
            if not draw_map.get(state):
                bliz_num = 0
                for _ in range(4):
                    bliz_num += state & 1
                    state >>= 1
                print(bliz_num, end='')
                continue
            print(draw_map.get(state), end='')
        print()
    print()

def new_generation(generation: dict, dimensions) -> dict:
    new_generation = {}
    for cell in generation:
        new_generation[cell] = 0
        for offset, state in neighbors.items():
            check_cell = np.array(cell) + offset
            new_generation[cell] |= generation.get(tuple(check_cell % dimensions), 0) & state
            new_generation[cell] |= generation.get(tuple(check_cell), 0) & STATE_ELF
        new_generation[cell] |= generation[cell] & STATE_ELF
        if new_generation[cell] - STATE_ELF > 0:
            new_generation[cell] ^= STATE_ELF

    return new_generation

def main():
    with open('24/input.txt', 'r') as f:
        input_lines = f.read().splitlines()

    generation = {(x, y): parse_map.get(char)
                  for y, line in enumerate(input_lines, -1)
                  for x, char in enumerate(line, -1)
                  if not char == '#'}

    width = len(input_lines[0][1:-1])
    height = len(input_lines[1:-1])
    start_pos = (0, -1)
    end_pos = (width-1, height)

    generation[start_pos] = STATE_ELF
    generation[end_pos] = 0

    gen_count = 0
    prev_tick = perf_counter()
    while True:
        if (tick := perf_counter()) - prev_tick > 0.1:
            os.system('clear')
            draw_scene(generation, (width, height))
            print('Generations:', gen_count)
            prev_tick = tick
        if generation.get(end_pos) == STATE_ELF:
            break
        generation = new_generation(generation, (width, height))
        gen_count += 1
    print('Minutes to end:', gen_count)

if __name__ == "__main__":
    start = perf_counter()
    main()
    end = perf_counter()
    print('Completed in:', round((end - start) * 1000, 2), 'ms')
