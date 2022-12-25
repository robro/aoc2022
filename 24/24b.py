#!/usr/bin/env python
import os
from math import lcm
from time import perf_counter
from collections import defaultdict
import numpy as np

max_time = 0 # No search can be longer than this. If 0, estimated automatically

BLIZ_MOVES = {
    '^': np.array([ 0,-1]),
    'v': np.array([ 0, 1]),
    '<': np.array([-1, 0]),
    '>': np.array([ 1, 0]),
}
E_MOVES = (
    np.array([ 1, 0]), # Right
    np.array([ 0, 1]), # Down
    np.array([ 0, 0]), # Wait
    np.array([ 0,-1]), # Up
    np.array([-1, 0]), # Left
)

class E:
    def __init__(self, pos, state_index=0, time=0, history=defaultdict(int)):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.state_index = state_index
        self.time = time
        self.history = history

def draw_scene(dimensions, obstacles: dict=None, E: E=None):
    width, height = dimensions
    for y in range(-1, height+1):
        for x in range(-1, width+1):
            if E and tuple(E.pos) == (x, y):
                print('E', end='')
            elif E and (visited := E.history.get((x, y))):
                # if visited >= 10:
                #     visited = 'M'
                # print(visited, end='')
                print('E', end='')
            elif obstacles and (ob_list := obstacles.get((x, y))):
                if len(ob_list) == 1:
                    print(ob_list[0], end='')
                else:
                    print(len(ob_list), end='')
            else:
                print('.', end='')
        print()

def get_new_obstacles(obstacles: dict, dimensions):
    new_obstacles = defaultdict(list)
    for pos, char_list in obstacles.items():
        for char in char_list:
            if char == '#':
                new_obstacles[pos].append(char)
            else:
                new_pos = (pos + BLIZ_MOVES[char]) % dimensions
                new_obstacles[tuple(new_pos)].append(char)
    return new_obstacles

def find_exit(start_E: E, end_pos, ob_states, dimensions):
    last_tick = perf_counter()
    queue = [start_E]
    visited_states = {start_E.state_index: {}}
    while queue:
        cur_E = queue.pop(0)
        cur_E.history[tuple(cur_E.pos)] += 1
        obstacles = ob_states[cur_E.state_index]
        if (cur_E.pos == end_pos).all():
            draw_scene(dimensions, obstacles, E=cur_E)
            return cur_E.time, cur_E.state_index
        cur_tick = perf_counter()
        if cur_tick - last_tick >= 0.1:
            os.system('clear')
            draw_scene(dimensions, E=cur_E)
            # draw_scene(dimensions, obstacles, E=cur_E)
            print('Current minute:', cur_E.time)
            print()
            last_tick = cur_tick
        if (not tuple(cur_E.pos) in obstacles and cur_E.y >= -1 and cur_E.y <= dimensions[1] and
                sum(end_pos - cur_E.pos) + cur_E.time <= max_time and
                not tuple(cur_E.pos) in visited_states.get(cur_E.state_index)):
            try:
                visited_states[cur_E.state_index][tuple(cur_E.pos)] = True
            except KeyError:
                visited_states[cur_E.state_index] = {tuple(cur_E.pos): True}
            for move in E_MOVES:
                new_pos = cur_E.pos + move
                new_state_index = (cur_E.state_index+1)%len(ob_states)
                queue.append(E(
                    new_pos, new_state_index, cur_E.time+1, cur_E.history.copy()))
                if not visited_states.get(new_state_index):
                    visited_states[new_state_index] = {}

def main():
    with open('24/input.txt', 'r') as f:
        input_lines = f.read().splitlines()

    print('Generating states...')
    obstacles = {(x,y): [char] for y, line in enumerate(input_lines, -1)
                 for x, char in enumerate(line, -1)
                 if not char == '.'}

    width = len(input_lines[0][1:-1])
    height = len(input_lines[1:-1])
    cycle_len = lcm(width, height)
    ob_states = []
    for _ in range(cycle_len):
        ob_states.append(obstacles)
        obstacles = get_new_obstacles(obstacles, (width, height))

    start_pos = np.array([0,-1])
    end_pos = np.array([width-1, height])
    global max_time
    if max_time == 0:
        max_time = sum(end_pos - start_pos) * 2

    print('Beginning search...')
    total_time = 0
    time, state_index = find_exit(E(np.array(start_pos)), end_pos, ob_states, (width, height))
    total_time += time
    time, state_index = find_exit(E(np.array(end_pos), state_index), start_pos, ob_states, (width, height))
    total_time += time
    time, _ = find_exit(E(np.array(start_pos), state_index), end_pos, ob_states, (width, height))
    total_time += time
    print(f'Time to end: {total_time} minutes')

if __name__ == "__main__":
    start = perf_counter()
    main()
    end = perf_counter()
    print('Completed in:', round((end - start) * 1000, 2), 'ms')
