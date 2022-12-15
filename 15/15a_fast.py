#!/usr/bin/env python

class Sensor:
    def __init__(self, x, y, b_x, b_y):
        self.x = x
        self.y = y
        self.b_x = b_x
        self.b_y = b_y
        self.b_dist = self.getDist(b_x, b_y)

    def getDist(self, x, y):
        return abs(self.x - x) + abs(self.y - y)

def mergeIntervals(inter, start_index = 0):
    for i in range(start_index, len(inter) - 1):
        if inter[i][1] > inter[i+1][0]:
            new_start = min(inter[i][0], inter[i+1][0])
            new_end = max(inter[i][1], inter[i+1][1])
            inter[i] = [new_start, new_end]
            del inter[i+1]
            return mergeIntervals(inter.copy(), start_index=i)
    return inter

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

    intervals = []
    occupied = set()
    row = 2000000
    for sensor in sensors:
        if sensor.b_y == row:
            occupied.add(sensor.b_x)
        if (y_dist := abs(sensor.y - row)) <= sensor.b_dist:
            x1 = sensor.x - (sensor.b_dist - y_dist)
            x2 = sensor.x + (sensor.b_dist - y_dist) + 1
            intervals.append([x1, x2])

    merged = mergeIntervals(sorted(intervals))
    signal = 0
    for interval in merged:
        signal += interval[1] - interval[0]

    no_beacon_pos = signal - len(occupied)
    print('Positions that cannot contain a beacon:', no_beacon_pos)

if __name__ == "__main__":
    main()
