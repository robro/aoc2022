#!/usr/bin/env python
import re
from time import time
from copy import copy
from math import ceil

class Blueprint:
    def __init__(self, num, costs: dict[str, dict[str, int]]):
        self.num = num
        self.costs = costs
        self.max_costs = {res: 0 for res in costs}
        for cost in self.costs.values():
            for res, amt in cost.items():
                self.max_costs[res] = max(self.max_costs[res], amt)
        self.max_costs['geode'] = float('inf')
        self.loops = 0
        self.max_state = None

    def find_max_geodes(self, t=0):
        bank = {res: 0 for res in self.costs}
        income = {res: 0 for res in self.costs}
        # Start with 1 ore robot
        income['ore'] = 1
        self.max_state = (t, bank, income)
        state = self._find_max_geodes((t, bank, income))
        print('Loops:', self.loops)
        print('Max geodes:', state[1]['geode'])
        return state[1]['geode']

    def _find_max_geodes(self, state: tuple[int, dict, dict]):
        t, bank, income = state
        if t <= 0:
            return state
        # Abort branch if it's impossible to beat the best branch
        max_geodes = bank['geode']
        for i in range(t):
            max_geodes += income['geode']+i
        if max_geodes <= self.max_state[1]['geode']:
            return state
        for rob, cost in self.costs.items():
            # Don't build robot if income is already as high as max cost
            if income[rob] >= self.max_costs[rob]:
                continue
            # Only build robots that will be built in time
            wt = 0 # Wait time. 0 = can build now
            for res, amt in cost.items():
                if income[res] == 0:
                    wt = float('inf')
                    break
                wt = max(wt, ceil((amt-bank[res]) / income[res]))
            if wt >= t:
                continue
            new_t = t - wt - 1
            new_bank = copy(bank)
            new_income = copy(income)
            # Add resources with respect to wait time
            for res, amt in income.items():
                new_bank[res] += amt * (wt+1)
            # Use resources to build robot
            for res, amt in cost.items():
                new_bank[res] -= amt
            new_income[rob] += 1
            new_state = self._find_max_geodes((new_t, new_bank, new_income))
            if new_state[1]['geode'] > state[1]['geode']:
                state = new_state

        if state[1]['geode'] > self.max_state[1]['geode']:
            self.max_state = state
        self.loops += 1
        return state

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

    # time_limit = 24
    time_limit = 32
    geode_product = 1
    for i, bp in enumerate(blueprints[0:3], start=1):
        print('Testing blueprint', i, 'of', len(blueprints[0:3]))
        cur_geodes = bp.find_max_geodes(time_limit)
        print()
        geode_product *= cur_geodes
    
    print('Product of geodes:', geode_product)


if __name__ == "__main__":
    start = time()
    main()
    end = time()
    print('Completed in:', round((end - start) * 1000, 2), 'ms')
