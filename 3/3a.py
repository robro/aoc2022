#!/usr/bin/env python
import string

priority = list(string.ascii_letters)

def main():
    with open('puzzle_input.txt', 'r') as sacks_file:
        sacks_lines = sacks_file.read().splitlines()

    priority_sum = 0
    for sack in sacks_lines:
        comp_1 = sack[:int(len(sack)/2)]
        comp_2 = sack[int(len(sack)/2):]
        shared_item = list(set(comp_1) & set(comp_2))[0]
        priority_sum += priority.index(shared_item) + 1

    print('Sum of priorities:', priority_sum)

if __name__ == "__main__":
    main()
