#!/usr/bin/env python
from time import perf_counter
import numpy as np

class Elf:
    def __init__(self, pos):
        self.id = str(pos)
        self.pos = pos
        self.proposal = None

    def is_alone(self, elves: list['Elf']):
        for elf in elves:
            if elf.id == self.id:
                continue
            if ((elf.pos >= self.pos-1) & (elf.pos <= self.pos+1)).all():
                return False
        return True

    def propose_move(self, elves: list['Elf'], proposals: list, positions, check_order):
        self.proposal = None
        for directions in check_order:
            occupied = False
            check_positions = self.pos + eval(directions)
            for elf in elves:
                if elf.id == self.id:
                    continue
                if (elf.pos == check_positions).all(1).any():
                    occupied = True
                    break
            if occupied:
                continue
            self.proposal = tuple(check_positions[1])
            proposals.append(self.proposal)
            return True
        return False

    def move_to_proposal(self):
        if not self.proposal:
            return
        self.pos = np.array(self.proposal)
        self.proposal = None

def get_bounds(elves):
    lo_x = float('inf')
    lo_y = float('inf')
    hi_x = float('-inf')
    hi_y = float('-inf')
    for elf in elves:
        lo_x = min(lo_x, elf.pos[0])
        lo_y = min(lo_y, elf.pos[1])
        hi_x = max(hi_x, elf.pos[0])
        hi_y = max(hi_y, elf.pos[1])

    return lo_x, lo_y, hi_x, hi_y

def draw_scene(elves: list['Elf'], bounds, round_num):
    lo_x, lo_y, hi_x, hi_y = bounds
    print('Round:', round_num)
    for y in range(lo_y, hi_y+1):
        for x in range(lo_x, hi_x+1):
            if (x,y) in [tuple(elf.pos) for elf in elves]:
                print('#', end='')
            else:
                print('.', end='')
        print()
    print()

def main():
    global elves
    with open('23/puzzle_input.txt', 'r') as f:
        input_lines = f.read().splitlines()

    elves = [Elf(np.array([x, y])) for y, line in enumerate(input_lines)
             for x, char in enumerate(line) if char == '#']
    
    proposals = []
    positions = np.array([
        [[-1,-1],[0,-1],[1,-1]],
        [[-1, 0],[0, 0],[1, 0]],
        [[-1, 1],[0, 1],[1, 1]]
    ])
    check_order = np.array([
        'positions[0]',   # north
        'positions[2]',   # south
        'positions[:,0]', # west
        'positions[:,2]'  # east
    ])

    rounds = 10
    bounds = None

    for round_num in range(1, rounds+1):
        # First half of round - The Proposals
        for elf in elves:
            if elf.is_alone(elves):
                continue
            elf.propose_move(elves, proposals, positions, check_order)

        # Second half of round - The Move
        for elf in elves:
            if elf.proposal and proposals.count(elf.proposal) > 1:
                continue
            elf.move_to_proposal()
        proposals = []
        check_order = np.roll(check_order, -1)
        bounds = get_bounds(elves)
        draw_scene(elves, bounds, round_num)
        # input('press enter')

    lo_x, lo_y, hi_x, hi_y = bounds
    print('Empty ground tiles:', (hi_x - lo_x+1) * (hi_y - lo_y+1) - len(elves))

if __name__ == "__main__":
    start = perf_counter()
    main()
    end = perf_counter()
    print('Completed in:', round((end - start) * 1000, 2), 'ms')
