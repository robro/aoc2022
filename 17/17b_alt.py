#!/usr/bin/env python
from time import time

total_rocks = 1000000000000
key_rocks = 450
spawn_offset_x = 2
spawn_offset_y = 3
cave_width = 7
tower_array = []
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

def get_tower_height(jet_str):
    global f_rock
    rocks_dropped = 0
    jet_index = 0
    shape_index = 0
    key_value = ()
    key_height = 0
    cycle_height = 0
    rocks_per_cycle = 0
    total_cycles = 0
    tower_height = 0

    while rocks_dropped < total_rocks:
        if not f_rock:
            shape = shapes[shape_index]
            f_rock = spawn_rock(shape, shape_tiles[shape])
            shape_index = 0 if shape_index == len(shapes)-1 else shape_index + 1
        else:
            if not f_rock.pushed:
                match jet_str[jet_index]:
                    case '<':
                        f_rock.move_left()
                    case '>':
                        f_rock.move_right()
                f_rock.pushed = True
                jet_index = 0 if jet_index == len(jet_str)-1 else jet_index + 1
            else:
                if f_rock.fall_down():
                    f_rock.pushed = False
                else:
                    f_rock.add_to_tower()
                    tower_height = max(tower_height, f_rock.y+1)
                    f_rock = None
                    rocks_dropped += 1
                    if rocks_dropped == key_rocks:
                        # Assume we're high enough to have started cycling
                        key_value = (shape_index, jet_index)
                        key_height = int(tower_height)
                    elif key_value and key_value == (shape_index, jet_index):
                        cycle_height = tower_height - key_height
                        rocks_per_cycle = rocks_dropped - key_rocks
                        total_cycles = (total_rocks - key_rocks) // rocks_per_cycle
                        # Skip to end of last cycle to finish tower
                        rocks_dropped = total_rocks - (
                            (total_rocks - key_rocks) % rocks_per_cycle)

    tower_height += cycle_height * (total_cycles - 1)
    return tower_height

def main():
    with open('puzzle_input.txt', 'r') as f:
        input_str = f.read()

    tower_height = get_tower_height(input_str)
    draw_scene()
    print('Total rocks:', total_rocks)
    print('Tower height:', tower_height)

if __name__ == "__main__":
    start = time()
    main()
    end = time()
    print('Completed in:', round((end - start) * 1000, 2), 'ms')
