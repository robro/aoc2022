#!/usr/bin/env python

class Sensor:
    def __init__(self, x, y, b_x, b_y):
        self.x = x
        self.y = y
        self.b_x = b_x
        self.b_y = b_y
        self.b_dist = self.getDistance(b_x, b_y)
        self.min_x = x - self.b_dist
        self.min_y = y - self.b_dist
        self.max_x = x + self.b_dist
        self.max_y = y + self.b_dist

    def getDistance(self, x, y):
        return abs(self.x - x) + abs(self.y - y)

def main():
    with open('puzzle_input.txt', 'r') as f:
        input_lines = f.read().splitlines()

    sensors: list[Sensor] = []
    strip_chars = 'xy=,:'
    for line in input_lines:
        items = line.split()
        x = int(items[2].strip(strip_chars))
        y = int(items[3].strip(strip_chars))
        b_x = int(items[8].strip(strip_chars))
        b_y = int(items[9].strip(strip_chars))
        sensors.append(Sensor(x, y, b_x, b_y))

    min_x = 0
    max_x = 0
    for sensor in sensors:
        if sensor.min_x < min_x: min_x = sensor.min_x
        if sensor.max_x > max_x: max_x = sensor.max_x

    # Brute force baby!
    y = 2000000
    no_beacon_pos = 0
    for x in range(min_x, max_x+1):
        not_occupied = True
        # Make sure we're not on any beacons or sensors
        for sensor in sensors:
            if ((x, y) == (sensor.b_x, sensor.b_y) or
                    (x, y) == (sensor.x, sensor.y)):
                not_occupied = False
                break
        if not_occupied:
            for sensor in sensors:
                if sensor.getDistance(x, y) <= sensor.b_dist:
                    no_beacon_pos += 1
                    break

    print('Positions that cannot contain a beacon:', no_beacon_pos)

if __name__ == "__main__":
    main()
