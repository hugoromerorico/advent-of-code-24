data = [line.strip() for line in open("in.txt") if line.strip()]

width = len(data[0])
height = len(data)

antennas = {}
for y in range(height):
    for x in range(width):
        c = data[y][x]
        if c != '.':
            if c not in antennas:
                antennas[c] = []
            antennas[c].append((x,y))

antinodes = set()
for freq, positions in antennas.items():
    for i in range(len(positions)):
        for j in range(i+1, len(positions)):
            x1,y1 = positions[i]
            x2,y2 = positions[j]
            
            # Calculate two potential antinode positions for each pair
            dx = x2 - x1
            dy = y2 - y1
            dist = ((dx**2 + dy**2)**0.5)
            
            # Point that is twice as far from x1,y1
            ax1 = x1 + 2*dx
            ay1 = y1 + 2*dy
            
            # Point that is twice as far from x2,y2  
            ax2 = x2 - 2*dx
            ay2 = y2 - 2*dy
            
            # Add antinodes if in bounds
            if 0 <= ax1 < width and 0 <= ay1 < height:
                antinodes.add((round(ax1), round(ay1)))
            if 0 <= ax2 < width and 0 <= ay2 < height:
                antinodes.add((round(ax2), round(ay2)))

# Add overlapping antenna positions as antinodes
seen_positions = set()
for freq, positions in antennas.items():
    for pos in positions:
        if pos in seen_positions:
            antinodes.add(pos)
        seen_positions.add(pos)

print(len(antinodes))