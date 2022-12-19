#!/usr/bin/env python
from time import time
from operator import add

# 3-D coords = (x, y, z)
offsets = (
    (-1, 0, 0), # left
    (1, 0, 0), # right
    (0, 1, 0), # up
    (0, -1, 0), # down
    (0, 0, 1), # front
    (0, 0, -1) # back
)
    
def main():
    with open('puzzle_input.txt', 'r') as f:
        input_lines = f.read().splitlines()

    lava_voxels = [(eval(l)) for l in input_lines]
    exposed_sides = 0
    for voxel in lava_voxels:
        for offset in offsets:
            if tuple(map(add, voxel, offset)) in lava_voxels:
                continue
            exposed_sides += 1
    print("Exposed sides:", exposed_sides)

if __name__ == "__main__":
    start = time()
    main()
    end = time()
    print('Completed in:', round((end - start) * 1000, 2), 'ms')
