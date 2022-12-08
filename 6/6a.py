#!/usr/bin/env python

def main():
    with open('puzzle_input.txt', 'r') as input_file:
        input_buffer = input_file.read().splitlines()[0]

    marker_length = 4
    for index in range(len(input_buffer)):
        window = input_buffer[index : index + marker_length]
        if len(set(window)) == marker_length:
            print("Characters processed:", index + marker_length)
            break

if __name__ == "__main__":
    main()
