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

    elves_total_calories.sort(reverse=True)
    top3_total_calories = 0
    for index in range(3):
        top3_total_calories += elves_total_calories[index]

    print('Total calories of top 3 elves:', top3_total_calories)

if __name__ == "__main__":
    main()
