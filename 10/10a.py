#!/usr/bin/env python

def getSignalStrength(at_cycle, instructions: list[str]):
    x = 1
    index = 0
    wait_time = 0
    x_change = 0
    for _ in range(at_cycle):
        if wait_time == 0:
            x += x_change
            x_change = 0
            parts = instructions[index].split()
            opcode = parts[0]
            if len(parts) > 1:
                value = parts[1]
            if opcode == 'noop':
                pass
            elif opcode == 'addx':
                wait_time = 1
                x_change = int(value)
            index += 1
        else:
            wait_time -= 1

    return x * at_cycle

def main():
    with open('puzzle_input.txt', 'r') as input_file:
        input_lines = input_file.read().splitlines()

    probe_cycles = list(range(20,221,40))
    signal_strength_sum = 0
    for cycle in probe_cycles:
        signal_strength_sum += getSignalStrength(cycle, input_lines)

    print('Signal strength sum:', signal_strength_sum)

if __name__ == "__main__":
    main()
