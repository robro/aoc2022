#!/usr/bin/env python
from time import time

def main():
    with open('puzzle_input.txt', 'r') as f:
        input_lines = f.read().splitlines()

    int_list = [int(line) for line in input_lines]
    paired_list = [(i, n) for i, n in enumerate(int_list)]
    seq_length = len(int_list)
    for i in range(seq_length):
        start_index = None
        for index, pair in enumerate(paired_list):
            if pair[0] == i:
                start_index = index
                index_shift = pair[1]
                break
        if start_index is None:
            print('Value not found:', index_shift)
            return -1
        shifted_index = (start_index + index_shift) % (seq_length-1)
        paired_list.insert(shifted_index, paired_list.pop(start_index))

    mixed_int_list = [pair[1] for pair in paired_list]
    zero_index = mixed_int_list.index(0)
    coord_1 = mixed_int_list[(zero_index+1000) % seq_length]
    coord_2 = mixed_int_list[(zero_index+2000) % seq_length]
    coord_3 = mixed_int_list[(zero_index+3000) % seq_length]
    print('Sum of coordinates:', coord_1 + coord_2 + coord_3)

if __name__ == "__main__":
    start = time()
    main()
    end = time()
    print('Completed in:', round((end - start) * 1000, 2), 'ms')
