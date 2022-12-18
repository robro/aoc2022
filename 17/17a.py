#!/usr/bin/env python
from time import time
from itertools import cycle

rock_count = 2022
spawn_x = 2
spawn_y = 3
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
    def __init__(self, x, y, tiles):
        self.x = x
        self.y = y
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
        for y in range(f_rock.height):
            for x in range(f_rock.width):
                try:
                    if (tower_array[check_y-y][check_x+x] == 1
                            and f_rock.tiles[y][x] == 1):
                        return True
                except IndexError:
                    pass
        return False

f_rock: Rock = None

def spawn_rock(tiles):
    return Rock(spawn_x, spawn_y + len(tower_array) + len(tiles)-1, tiles)

def add_to_tower():
    global f_rock
    global rock_count
    global tower_array
    # Extend tower array to fit the rock if neccessary
    tower_array += [
        [0]*cave_width for _ in range((f_rock.y+1) - len(tower_array))]
    # Add rock tiles to tower array
    for y in range(f_rock.height):
        for x in range(f_rock.width):
            if f_rock.tiles[y][x] == 1:
                tower_array[f_rock.y-y][f_rock.x+x] = 1
    rock_count -= 1
    f_rock = None

def draw_scene(draw_height=10):
    tower_height = len(tower_array)
    # Get draw range
    if draw_height == 0:
        draw_height = max(tower_height, f_rock.y+1) if f_rock else tower_height
    # Draw some ASCII art
    for y in range(draw_height-1, -1, -1):
        print('|', end='')
        for x in range(cave_width):
            if (f_rock and x >= f_rock.x and x < f_rock.x+f_rock.width and
                y <= f_rock.y and y > f_rock.y-f_rock.height and
                f_rock.tiles[f_rock.y-y][x-f_rock.x] == 1):
                    print('@', end='')
            elif y < tower_height and tower_array[y][x] == 1:
                    print('#', end='')
            else:
                print('.', end='')
        print('|')
    print('+' + '-'*cave_width + '+')
    print()

def main():
    global rock_count
    global f_rock
    global tower_array

    with open('puzzle_input.txt', 'r') as f:
        input_str = f.read()

    jet_loop = cycle(input_str)
    shape_loop = cycle(shapes)

    while rock_count > 0:
        if not f_rock:
            f_rock = spawn_rock(shape_tiles[next(shape_loop)])
        else:
            if not f_rock.pushed:
                match next(jet_loop):
                    case '<':
                        f_rock.move_left()
                    case '>':
                        f_rock.move_right()
                f_rock.pushed = True
            else:
                if not f_rock.fall_down():
                    add_to_tower()
                else:
                    f_rock.pushed = False
    draw_scene()
    print('Tower height:', len(tower_array))

if __name__ == "__main__":
    start = time()
    main()
    end = time()
    print(round((end - start) * 1000, 2), 'ms')
