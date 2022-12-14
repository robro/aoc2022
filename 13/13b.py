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
    for line in input_lines:
        if line:
            packets.append(eval(line)) # DANGER!
    packets.append([[2]])
    packets.append([[6]])

    i = 1
    while i < len(packets):
        j = i
        while j > 0 and comparePackets(packets[j-1], packets[j]) is False:
            packets[j-1], packets[j] = packets[j], packets[j-1]
            j -= 1
        i += 1

    print('Decoder key:', (packets.index([[2]])+1) * (packets.index([[6]])+1))

if __name__ == "__main__":
    main()
