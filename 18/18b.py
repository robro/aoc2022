#!/usr/bin/env python
from time import time
from operator import add, sub, ge, lt

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

    droplet = [(eval(l)) for l in input_lines]

    vec_lo = [float('inf')]*3
    vec_hi = [0]*3

    for vec in droplet:
        for i in range(len(vec)):
            vec_lo[i] = min(vec_lo[i], vec[i])
            vec_hi[i] = max(vec_hi[i], vec[i])

    bound_lo = tuple([x-2 for x in vec_lo])
    bound_hi = tuple([x+2 for x in vec_hi])
    bound_l, bound_h, bound_b = tuple(map(sub, bound_hi, bound_lo))
    bound_sfa = 2 * (bound_l*bound_b + bound_b*bound_h + bound_l*bound_h)

    # Explore all "air" around droplet
    queue = [bound_lo]
    explored = [bound_lo]
    while queue:
        cur_vec = queue.pop(0)
        for offset in offsets:
            adj_vec = tuple(map(add, cur_vec, offset))
            # Only check inside bounds
            if (all(tuple(map(ge, adj_vec, bound_lo))) and
                    all(tuple(map(lt, adj_vec, bound_hi)))):
                if not adj_vec in explored and not adj_vec in droplet:
                    explored.append(adj_vec)
                    queue.append(adj_vec)

    # Get exposed area of "air"
    exposed_sides = 0
    for vec in explored:
        for offset in offsets:
            if tuple(map(add, vec, offset)) in explored:
                continue
            exposed_sides += 1

    # And subtract the outer surface area of the "air" prism
    exposed_sides -= bound_sfa
    print("Exposed sides:", exposed_sides)

if __name__ == "__main__":
    start = time()
    main()
    end = time()
    print('Completed in:', round((end - start) * 1000, 2), 'ms')
