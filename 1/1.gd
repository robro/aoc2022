#!/usr/bin/env -S godot -s
extends SceneTree

func _init():
    var input_file = File.new()
    input_file.open("puzzle_input.txt", File.READ)
    var input_lines = input_file.get_as_text().split('\n')
    input_file.close()

    var elf_calories = 0
    var elves_total_calories = []
    for line in input_lines:
        if line:
            elf_calories += int(line)
        else:
            elves_total_calories.append(elf_calories)
            elf_calories = 0
    elves_total_calories.append(elf_calories)

    print("Most calories: ", elves_total_calories.max())
    elves_total_calories.sort()
    print(
        "Top 3 combined total: ",
        elves_total_calories.pop_back() +
        elves_total_calories.pop_back() +
        elves_total_calories.pop_back())
    quit()