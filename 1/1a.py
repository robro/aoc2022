#!/usr/bin/env python

def main():
    with open('puzzle_input.txt', 'r') as elves_calories_file:
        elves_calories_list = elves_calories_file.read().splitlines()

    elves_total_calories = []
    elf_calories = 0
    for i, line in enumerate(elves_calories_list):
        if line == '':
            if elf_calories > 0:
                elves_total_calories.append(elf_calories)
                elf_calories = 0
        else:
            elf_calories += int(line)
            if i == len(elves_calories_list)-1:
                elves_total_calories.append(elf_calories)
                elf_calories = 0

    most_calories = 0
    elf_with_most = {
        'pos': None,
        'cal': None
    }
    for elf_num, elf_calories in enumerate(elves_total_calories, start=1):
        if elf_calories > most_calories:
            most_calories = elf_calories
            elf_with_most['pos'] = elf_num
            elf_with_most['cal'] = most_calories

    print('Elf carrying the most calories:', elf_with_most['pos'])
    print('They are carrying:', elf_with_most['cal'], 'calories')

if __name__ == "__main__":
    main()
