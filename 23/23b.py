#!/usr/bin/env python
from time import perf_counter
from collections import defaultdict
import numpy as np

def get_bounds(elves):
    lo_x = float('inf')
    lo_y = float('inf')
    hi_x = float('-inf')
    hi_y = float('-inf')
    for elf in elves:
        lo_x = min(lo_x, elf[0])
        lo_y = min(lo_y, elf[1])
        hi_x = max(hi_x, elf[0])
        hi_y = max(hi_y, elf[1])
    return lo_x, lo_y, hi_x, hi_y

def draw_scene(elves: dict, bounds):
    lo_x, lo_y, hi_x, hi_y = bounds
    for y in range(lo_y, hi_y+1):
        for x in range(lo_x, hi_x+1):
            if elves.get((x, y)):
                print('#', end='')
            else:
                print('.', end='')
        print()
    print()

def propose_move(elf, elves: dict, proposals, check_directions):
    proposal = None
    is_alone = True
    for direction in check_directions:
        check_positions = elf + direction
        for pos in check_positions:
            if elves.get(tuple(pos)):
                is_alone = False
                break
        else:
            if not proposal:
                proposal = tuple(check_positions[1])
    if is_alone or not proposal:
        return False
    proposals[proposal].append(elf)
    return True

def main():
    with open('23/puzzle_input.txt', 'r') as f:
        input_lines = f.read().splitlines()

    elves = {(x, y): True for y, line in enumerate(input_lines)
             for x, char in enumerate(line)
             if char == '#'}
    proposals = defaultdict(list)
    check_directions = np.array([
        [[-1,-1],[ 0,-1],[ 1,-1]], # North
        [[-1, 1],[ 0, 1],[ 1, 1]], # South
        [[-1,-1],[-1, 0],[-1, 1]], # West
        [[ 1,-1],[ 1, 0],[ 1, 1]], # East
    ])
    need_to_move = True
    total_rounds = 0

    while need_to_move:
        total_rounds += 1
        print('Round started:', total_rounds)
        need_to_move = False
        for elf in elves:
            if propose_move(elf, elves, proposals, check_directions):
                need_to_move = True
        if not need_to_move:
            break
        for proposal, elf in proposals.items():
            if len(elf) > 1:
                continue
            del elves[elf[0]]
            elves[proposal] = True
        proposals.clear()
        check_directions = np.roll(check_directions, -1, axis=0)
        draw_scene(elves, get_bounds(elves))

    print('Total rounds:', total_rounds)

if __name__ == "__main__":
    start = perf_counter()
    main()
    end = perf_counter()
    print('Completed in:', round((end - start) * 1000, 2), 'ms')
