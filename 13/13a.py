#!/usr/bin/env python

def comparePackets(p1, p2):
    for i in range(len(p1) if len(p1) > len(p2) else len(p2)):
        if i >= len(p1):
            return True
        if i >= len(p2):
            return False
        item1 = p1[i]
        item2 = p2[i]
        if type(item1) == int and type(item2) == int:
            if item1 < item2:
                return True
            elif item1 > item2:
                return False
        else:
            if type(item1) == int:
                item1 = [item1]
            elif type(item2) == int:
                item2 = [item2]
            comp_result = comparePackets(item1, item2)
            if comp_result is True or comp_result is False:
                return comp_result
    return None

def main():
    with open('puzzle_input.txt', 'r') as f:
        input_lines = f.read().splitlines()

    packets = []
    pair = []
    for line in input_lines:
        if line:
            pair.append(eval(line)) # DANGER!
        else:
            packets.append(pair)
            pair = []
    packets.append(pair)

    indices_sum = 0
    for index, pair in enumerate(packets, start=1):
        if comparePackets(pair[0], pair[1]) is True:
            indices_sum += index

    print('Sum of indices:', indices_sum)

if __name__ == "__main__":
    main()
