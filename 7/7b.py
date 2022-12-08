#!/usr/bin/env python
import re
from pathlib import PurePath

def main():
    with open('puzzle_input.txt', 'r') as input_file:
        input_lines = input_file.read().splitlines()

    files = []
    dirs = []
    cur_dir = PurePath('/')
    dirs.append(str(cur_dir))
    for line in input_lines:
        if (dir_name := re.match(r'\$ cd (\w+)', line)):
            cur_dir /= dir_name.group(1)
            dirs.append(cur_dir)
        elif line == '$ cd ..':
            cur_dir = cur_dir.parent
        elif (file_info := re.match(r'(\d+) (\S+)', line)):
            files.append(
                (cur_dir / file_info.group(2), int(file_info.group(1))))

    total_sizes = []
    for dir in dirs:
        total_size = 0
        for file in files:
            file_path, file_size = file
            if file_path.is_relative_to(dir):
                total_size += file_size
        total_sizes.append(total_size)

    total_sizes.sort(reverse=True)
    free_space = 70000000 - total_sizes[0]
    space_needed = 30000000 - free_space
    total_sizes.sort()
    for size in total_sizes:
        if size >= space_needed:
            print('Size of directory to delete:', size)
            break

if __name__ == "__main__":
    main()
