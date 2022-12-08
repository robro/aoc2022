#!/usr/bin/env python

def main():
    with open('puzzle_input.txt', 'r') as input_file:
        input_lines = input_file.read().splitlines()

    stack_list = [[] for _ in range(9)]

    for line in input_lines[:8]:
        for column in range(9):
            index = column * 4
            crate = line[index : index+4].strip('[] ')
            if crate:
                stack_list[column].append(crate)
    
    for line in input_lines[10:]:
        line_items = line.split()
        move_num = int(line_items[1])
        from_num = int(line_items[3])
        to_num = int(line_items[5])
        stack_list[to_num-1][:0] = stack_list[from_num-1][:move_num]
        stack_list[from_num-1] = stack_list[from_num-1][move_num:]

    top_crates = ''.join([stack[0] for stack in stack_list])
    print('Top crates:', top_crates)

if __name__ == "__main__":
    main()
