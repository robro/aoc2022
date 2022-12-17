#!/usr/bin/env python
from time import time

class Valve:
    def __init__(self, id, flow_rate, neighbors):
        self.id = id
        self.flow_rate = flow_rate
        self.neighbors = neighbors
        self.parent = None
        self.dist_to: dict[Valve, int] = {}

valves: dict[str, Valve] = {}
time_limit = 30
start_id = 'AA'
most_release = 0

def find_release(valve_list: list[Valve], parent: Valve, time=time_limit, release=0):
    new_release = release
    global most_release
    for valve in valve_list:
        sub_list = list(valve_list)
        sub_list.remove(valve)
        new_time = time - parent.dist_to[valve] - 1
        if new_time > 0:
            new_release = release + (valve.flow_rate * new_time)
            new_release = find_release(sub_list, valve, new_time, new_release)
        most_release = max(most_release, new_release)
    return new_release

def main():
    with open('puzzle_input.txt', 'r') as f:
        input_lines = f.read().splitlines()

    # Populate dict of all valves
    for line in input_lines:
        items = line.split()
        id = items[1]
        flow_rate = int(items[4].strip('rate=;'))
        neighbors = tuple(v.strip(',') for v in items[9:])
        valves[id] = Valve(id, flow_rate, neighbors)

    root_valve = valves[start_id]
    flow_valves = [v for v in valves.values() if v.flow_rate > 0]

    # Get shortest distance between all valves
    for start_valve in valves.values():
        for end_valve in valves.values():
            queue = [start_valve]
            tested = [start_valve]
            while queue:
                cur_valve = queue.pop(0)
                if cur_valve == end_valve:
                    distance = 0
                    while cur_valve != start_valve:
                        cur_valve = cur_valve.parent
                        distance += 1
                    start_valve.dist_to[end_valve] = distance
                    break
                for neighbor_id in cur_valve.neighbors:
                    if (neighbor := valves[neighbor_id]) not in tested:
                        neighbor.parent = cur_valve
                        tested.append(neighbor)
                        queue.append(neighbor)

    # Release me!
    find_release(flow_valves, root_valve)
    print('Most pressure possible to release:', most_release)

if __name__ == "__main__":
    start = time()
    main()
    end = time()
    print(round((end - start) * 1000, 2), 'ms')
