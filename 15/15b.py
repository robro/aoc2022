#!/usr/bin/env python

class Sensor:
    def __init__(self, x, y, b_x, b_y):
        self.x = x
        self.y = y
        self.b_x = b_x
        self.b_y = b_y
        self.b_dist = self.getDist(b_x, b_y)
        self.min_x = x - self.b_dist
        self.min_y = y - self.b_dist
        self.max_x = x + self.b_dist
        self.max_y = y + self.b_dist

    def getDist(self, x, y):
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

    group: list[Sensor] = []
    for sensor1 in sensors:
        if sensor1 in group:
            continue
        for sensor2 in sensors:
            if sensor1 is sensor2:
                continue
            if sensor2 in group or sensor1 in group:
                continue
            distance = sensor1.getDist(sensor2.x, sensor2.y)
            if distance == sensor1.b_dist + sensor2.b_dist + 2:
                group.append(sensor1)
                group.append(sensor2)

    # oh god I have to do math!

    # find the line segments
    x1 = group[0].x
    y1 = group[0].y
    if group[0].y < group[1].y:
        y1 += group[0].b_dist + 1
    else:
        y1 -= group[0].b_dist + 1

    x2 = group[0].x
    y2 = group[0].y
    if group[0].x < group[1].x:
        x2 += group[0].b_dist + 1
    else:
        x2 -= group[0].b_dist + 1

    x3 = group[2].x
    y3 = group[2].y
    if group[2].y < group[3].y:
        y3 += group[2].b_dist + 1
    else:
        y3 -= group[2].b_dist + 1

    x4 = group[2].x
    y4 = group[2].y
    if group[2].x < group[3].x:
        x4 += group[2].b_dist + 1
    else:
        x4 -= group[2].b_dist + 1

    # do some freakin math
    m1 = (y2 - y1) / (x2 - x1)
    m2 = (y4 - y3) / (x4 - x3)
    b1 = y1 - m1 * x1
    b2 = y3 - m2 * x3
    xi = (b1 - b2) / (m2 - m1)
    yi = m1 * xi + b1

    print('Tuning frequency:', int(xi * 4000000 + yi))

if __name__ == "__main__":
    main()
