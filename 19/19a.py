#!/usr/bin/env python
import re
from time import time
from copy import copy
from math import ceil

# For each blueprint, find the optimal decision tree to maximize the amount
# of obsidian after 24 minutes.
#
# Decision trees are based on what is currently possible, as well as what will
# become possible in the future.
#
# You can't simply choose an option as soon as it's available, because then
# you would always build the cheapest robot and ignore possiblities that
# involve saving up resources.
#
# Choosing to build a robot may open up new decision trees. For instance,
# you will never be able to build an obsidian robot until you first build
# a clay robot.

# Keep track of when resources become "infinite". Meaning that with the current
# amount plus the amount that will be produced by the current robots before the
# time limit, you will never run out of that resource even if you make a robot
# that uses the most of that resource every minute until the end.

# When a resource becomes "infinite", build no more robots of that type.

# Always build a robot as soon as you have the resources to do so. It is not
# optimal to pass on building robot X now, if you are not waiting specifially
# to build robot Y.

class Blueprint:
    def __init__(self, num, costs: dict[str, dict[str, int]]):
        self.num = num
        self.costs = costs
        self.max_resource_costs = {res: 0 for res in self.costs}
        for costs in self.costs.values():
            for res, cost in costs.items():
                self.max_resource_costs[res] = max(
                    self.max_resource_costs[res], cost)
        self.max_resource_costs['geode'] = float('inf')
        self.tests = 0

    def find_max_quality(self, time_limit):
        resources = {res: 0 for res in self.costs}
        robots = {res: 0 for res in self.costs}
        # Start with 1 ore robot
        robots['ore'] = 1
        max_state = self._find_max_geodes(
            (time_limit, copy(resources), copy(robots)))
        print('Tests:', self.tests)
        print('Max geodes:', max_state[1]['geode'])
        return max_state[1]['geode'] * self.num

    def _find_max_geodes(self, state):
        max_state = copy(state)
        time_remaining, resources, robots = state
        if time_remaining > 0:
            for robot_type in self.costs:
                # Do I need to build any more?
                if resources[robot_type] == float('inf'):
                    continue
                # Can I build one before time runs out?
                wait_time = 0
                for res, cost in self.costs[robot_type].items():
                    if robots[res] == 0:
                        wait_time = float('inf')
                        break
                    else:
                        wait_time = max(ceil(max(0, (cost - resources[res])) / 
                            robots[res]), wait_time)
                if wait_time >= time_remaining:
                    continue
                new_time = int(time_remaining - wait_time)
                new_resources = copy(resources)
                new_robots = copy(robots)
                # Update resources
                for res in new_resources:
                    new_resources[res] += new_robots[res] * (wait_time+1)
                    # Mark resource that can't be depleted in time as infinite
                    if new_resources[res] >= (
                            self.max_resource_costs[res] * time_remaining):
                        new_resources[res] = float('inf')
                # Use resources to start production
                for res, cost in self.costs[robot_type].items():
                    new_resources[res] -= cost
                new_robots[robot_type] += 1
                new_state = self._find_max_geodes((
                    new_time-1, new_resources, new_robots))
                if new_state[1]['geode'] > max_state[1]['geode']:
                    max_state = new_state

        self.tests += 1
        return max_state

def main():
    with open('puzzle_input.txt', 'r') as f:
        input_lines = f.read().splitlines()

    blueprints: list[Blueprint] = []
    for line in input_lines:
        num = int(re.search(r'Blueprint (\d+)', line).group(1))
        cost_strings = re.findall(r'Each[^\.]+\.', line)
        costs = {}
        for string in cost_strings:
            costs[re.search(r'Each (\S+)', string).group(1)] = {
                f[1]: int(f[0]) for f in re.findall(r'(\d+) ([^\.\s]+)', string)}
        blueprints.append(Blueprint(num, costs))

    time_limit = 24
    total_quality = 0
    for i, bp in enumerate(blueprints, start=1):
        print('Testing blueprint', i, 'of', len(blueprints))
        cur_quality = bp.find_max_quality(time_limit)
        print('Quality:', cur_quality)
        print()
        total_quality += cur_quality
    
    print('Sum of quality:', total_quality)


if __name__ == "__main__":
    start = time()
    main()
    end = time()
    print('Completed in:', round((end - start) * 1000, 2), 'ms')
