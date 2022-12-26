#!/usr/bin/env python
import os
from time import perf_counter
import numpy as np

cell_state = {
    'ELF': int('10000', 2),
    'UP': int('01000', 2),
    'RIGHT': int('00100', 2),
    'DOWN': int('00010', 2),
    'LEFT': int('00001', 2)
}

parse_map = {
    '^': cell_state['UP'],
    '>': cell_state['RIGHT'],
    'v': cell_state['DOWN'],
    '<': cell_state['LEFT'],
    '.': 0
}
draw_map = {
    cell_state['ELF']: 'E',
    cell_state['UP']: '^',
    cell_state['RIGHT']: '>',
    cell_state['DOWN']: 'v',
    cell_state['LEFT']: '<',
    0: '.'
}
neighbors = {
    ( 0,-1): cell_state['DOWN'],
    ( 1, 0): cell_state['LEFT'],
    ( 0, 1): cell_state['UP'],
    (-1, 0): cell_state['RIGHT']
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
            if generation.get(tuple((np.array(cell) + offset) % dimensions)) & state:
                new_generation[cell] |= state
        if new_generation[cell] > 0:
            continue
        if generation[cell] == cell_state['ELF']:
            new_generation[cell] = cell_state['ELF']
            continue
        for offset in neighbors:
            if generation.get(tuple((np.array(cell) + offset))) == cell_state['ELF']:
                new_generation[cell] = cell_state['ELF']

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

    generation[start_pos] = cell_state['ELF']
    generation[end_pos] = 0

    gen_count = 0
    prev_tick = perf_counter()
    while True:
        if (tick := perf_counter()) - prev_tick > 0.1:
            os.system('clear')
            draw_scene(generation, (width, height))
            print('Generations:', gen_count)
            prev_tick = tick
        if generation.get(end_pos) == cell_state['ELF']:
            break
        generation = new_generation(generation, (width, height))
        gen_count += 1
    print('Minutes to end:', gen_count)

if __name__ == "__main__":
    start = perf_counter()
    main()
    end = perf_counter()
    print('Completed in:', round((end - start) * 1000, 2), 'ms')
