#!/usr/bin/env python
from time import time

def get_shifted_index(start_index, index_shift, seq_length):
    shifted_index = start_index + index_shift
    mod_value = seq_length-1
    if shifted_index == 0 and index_shift != 0:
        return mod_value
    return shifted_index % mod_value

def shift_list(paired_list: list[tuple]):
    seq_length = len(paired_list)
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
        shifted_index = get_shifted_index(start_index, index_shift, seq_length)
        paired_list.insert(shifted_index, paired_list.pop(start_index))

def main():
    with open('puzzle_input.txt', 'r') as f:
        input_lines = f.read().splitlines()

    key = 811589153
    int_list = [int(line)*key for line in input_lines]
    paired_list = [(i, n) for i, n in enumerate(int_list)]
    for _ in range(10):
        shift_list(paired_list)

    mixed_int_list = [pair[1] for pair in paired_list]
    zero_index = mixed_int_list.index(0)
    coord_1 = mixed_int_list[(zero_index+1000) % len(int_list)]
    coord_2 = mixed_int_list[(zero_index+2000) % len(int_list)]
    coord_3 = mixed_int_list[(zero_index+3000) % len(int_list)]
    print('Sum of coordinates:', coord_1 + coord_2 + coord_3)

if __name__ == "__main__":
    start = time()
    main()
    end = time()
    print('Completed in:', round((end - start) * 1000, 2), 'ms')
