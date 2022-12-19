#!/usr/bin/env python
from time import time
from itertools import cycle

total_rocks = 1000000000000
max_drop = 5000
spawn_offset_x = 2
spawn_offset_y = 3
cave_width = 7
tower_array = []
rock_values = []
shapes = '-+L|o'
shape_tiles = {
    '-': [
        [1,1,1,1]],
    '+': [
        [0,1,0],
        [1,1,1],
        [0,1,0]],
    'L': [
        [0,0,1],
        [0,0,1],
        [1,1,1]],
    '|': [
        [1],
        [1],
        [1],
        [1]],
    'o': [
        [1,1],
        [1,1]]
}

class Rock:
    def __init__(self, x, y, shape, tiles):
        self.x = x
        self.y = y
        self.shape = shape
        self.tiles = tiles
        self.width = len(tiles[0])
        self.height = len(tiles)
        self.pushed = False
    
    def move_left(self):
        if self.x == 0:
            return False
        if self.would_collide(-1, 0):
            return False
        self.x -= 1
        return True

    def move_right(self):
        if self.x + self.width == cave_width:
            return False
        if self.would_collide(1, 0):
            return False
        self.x += 1
        return True
 
    def fall_down(self):
        if self.y - self.height < 0:
            return False
        if self.would_collide(0, -1):
            return False
        self.y -= 1
        return True

    def would_collide(self, x_offset, y_offset):
        check_x = self.x + x_offset
        check_y = self.y + y_offset
        for y in range(self.height):
            for x in range(self.width):
                try:
                    if (tower_array[check_y-y][check_x+x] == 1
                            and self.tiles[y][x] == 1):
                        return True
                except IndexError:
                    pass
        return False

    def add_to_tower(self):
        global tower_array
        # Extend tower array to fit new rock if neccessary
        tower_array += [
            [0]*cave_width for _ in range((self.y+1) - len(tower_array))]
        # Add rock tiles to tower array
        for y in range(self.height):
            for x in range(self.width):
                if self.tiles[y][x] == 1:
                    tower_array[self.y-y][self.x+x] = 1

f_rock: Rock = None

def spawn_rock(shape, tiles):
    spawn_y = spawn_offset_y + len(tower_array) + len(tiles)-1
    return Rock(spawn_offset_x, spawn_y, shape, tiles)


def draw_scene(scene_height=10, min_y=0):
    # Draw some ASCII art
    for y in range(min_y+scene_height-1, min_y-1, -1):
        print('|', end='')
        for x in range(cave_width):
            if (f_rock and x >= f_rock.x and x < f_rock.x+f_rock.width and
                y <= f_rock.y and y > f_rock.y-f_rock.height and
                f_rock.tiles[f_rock.y-y][x-f_rock.x] == 1):
                    print('@', end='')
            elif y < len(tower_array) and tower_array[y][x] == 1:
                    print('#', end='')
            else:
                print('.', end='')
        print('|', y)
    if min_y == 0:
        print('+' + '-'*cave_width + '+')

def get_loop(seq):
    max_len = len(seq) // 2
    for x in range(2, max_len):
        if seq[:x] == seq[x:2*x]:
            return seq[:x]
    return []

def get_nonloop(seq, loop):
    loop_len = len(loop)
    temp_seq = seq[:]
    for _ in range(len(seq) // loop_len):
        if temp_seq[:loop_len] != loop:
            break
        temp_seq = temp_seq[loop_len:]
    return temp_seq

def get_tower_height(rocks_to_drop, jet_str):
    global f_rock
    global rock_values
    global tower_array
    jet_loop = cycle(jet_str)
    shape_loop = cycle(shapes)
    rocks_remaining = min(rocks_to_drop, max_drop)
    rock_values = []
    tower_array = []

    while rocks_remaining > 0:
        if not f_rock:
            shape = next(shape_loop)
            f_rock = spawn_rock(shape, shape_tiles[shape])
        else:
            if not f_rock.pushed:
                match next(jet_loop):
                    case '<':
                        f_rock.move_left()
                    case '>':
                        f_rock.move_right()
                f_rock.pushed = True
            else:
                if f_rock.fall_down():
                    f_rock.pushed = False
                else:
                    f_rock.add_to_tower()
                    # Save unique value to help identify the loop
                    rock_values.append(f_rock.x)
                    rocks_remaining -= 1
                    f_rock = None
    return len(tower_array)

def main():
    global rock_values
    with open('puzzle_input.txt', 'r') as f:
        input_str = f.read()

    tower_height = get_tower_height(total_rocks, input_str)
    rocks_tested = len(rock_values)
    draw_scene()

    if total_rocks > max_drop:
        # Find rock loop to extrapolate theoretical height
        rock_values.reverse()
        rock_loop = get_loop(rock_values)
        loop_height = len(get_loop(tower_array[-10::-1]))
        if rock_loop:
            rocks_per_loop = len(rock_loop)
            nonloop = get_nonloop(rock_values, rock_loop)
            nonloop_rocks = 0
            for i, value in enumerate(nonloop):
                if value != rock_loop[i]:
                    nonloop_rocks = len(nonloop) - i
                    break

            test_rocks = nonloop_rocks + (
                (total_rocks - nonloop_rocks) % rocks_per_loop)
            tower_height = get_tower_height(test_rocks, input_str) + \
                (((total_rocks - nonloop_rocks) // rocks_per_loop) * loop_height)

            print('Rocks tested:', rocks_tested)
            print('Loop starts at:', nonloop_rocks, 'rocks')
            print('Loop length:', rocks_per_loop, 'rocks')

    print('Total rocks:', total_rocks)
    print('Tower height:', tower_height)

if __name__ == "__main__":
    start = time()
    main()
    end = time()
    print('Completed in:', round((end - start) * 1000, 2), 'ms')
