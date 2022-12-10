#!/usr/bin/env python

def main():
    with open('puzzle_input.txt', 'r') as input_file:
        input_lines = input_file.read().splitlines()

    x = 1
    index = 0
    wait_time = 0
    x_change = 0
    crt_pos = 0

    while index < len(input_lines):
        if wait_time == 0:
            x += x_change
            x_change = 0
            match input_lines[index].split():
                case ['addx', n]:
                    wait_time = 1
                    x_change = int(n)
            index += 1
        else:
            wait_time -= 1

        # draw pixel
        if crt_pos >= x-1 and crt_pos <= x+1:
            print('#', end='')
        else:
            print('.', end='')
        crt_pos += 1
        crt_pos %= 40
        if crt_pos == 0:
            print('\n', end='')

if __name__ == "__main__":
    main()
