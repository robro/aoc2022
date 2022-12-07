#!/usr/bin/env python

def main():
    with open('puzzle_input.txt', 'r') as sections_file:
        sections_lines = sections_file.read().splitlines()

    total_overlap = 0
    for line in sections_lines:
        s1, s2 = line.split(',')
        s1_start, s1_end = s1.split('-')
        s2_start, s2_end = s2.split('-')
        s1_set = set(range(int(s1_start), int(s1_end)+1))
        s2_set = set(range(int(s2_start), int(s2_end)+1))
        overlap = s1_set & s2_set
        if overlap:
            total_overlap += 1

    print('Total pairs with overlapping ranges:', total_overlap)

if __name__ == "__main__":
    main()
