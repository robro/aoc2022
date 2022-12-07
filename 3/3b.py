#!/usr/bin/env python
import string

priority = list(string.ascii_letters)

def main():
    with open('puzzle_input.txt', 'r') as sacks_file:
        sacks_lines = sacks_file.read().splitlines()

    priority_sum = 0
    for i, sack in enumerate(sacks_lines):
        group_index = i % 3
        if group_index == 0:
            # first elf in group
            elf_group = []
        elf_group.append(sack)
        if group_index == 2:
            # third elf in group
            badge = list(
                set(elf_group[0]) &
                set(elf_group[1]) &
                set(elf_group[2]))[0]
            priority_sum += priority.index(badge) + 1

    print('Sum of priorities:', priority_sum)

if __name__ == "__main__":
    main()
