# advent-of-code-24/8_2/exec.py
data = [line.strip() for line in open("in.txt") if line.strip()]

width = len(data[0])
height = len(data)

from math import gcd

positions = {}
for y, line in enumerate(data):
    for x, c in enumerate(line):
        if c != '.':
            if c not in positions:
                positions[c] = []
            positions[c].append((x, y))

antinodes = set()

def generate_line_points(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    points = set()

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        # Same point
        points.add((x1, y1))
        return points

    step_x = dx // gcd(dx, dy) if dx != 0 else 0
    step_y = dy // gcd(dx, dy) if dy != 0 else 0

    # Extend the line in both directions within the grid bounds
    # Forward direction
    x, y = x2, y2
    while 0 <= x < width and 0 <= y < height:
        points.add((x, y))
        x += step_x
        y += step_y

    # Backward direction
    x, y = x1, y1
    while 0 <= x < width and 0 <= y < height:
        points.add((x, y))
        x -= step_x
        y -= step_y

    return points

for freq, antennas in positions.items():
    if len(antennas) < 2:
        continue

    # Include all antenna positions as antinodes
    antinodes.update(antennas)

    for i in range(len(antennas)):
        for j in range(i + 1, len(antennas)):
            line_points = generate_line_points(antennas[i], antennas[j])
            antinodes.update(p for p in line_points if 0 <= p[0] < width and 0 <= p[1] < height)

print(len(antinodes))