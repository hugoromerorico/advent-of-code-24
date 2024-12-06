data = [line.strip() for line in open("in.txt") if line.strip()]

# Find guard position and create grid
grid = []
start_pos = None
start_dir = None
for i, row in enumerate(data):
    grid_row = []
    for j, c in enumerate(row):
        if c in '^v<>':
            start_pos = (i,j)
            start_dir = '^v<>'.index(c)
            grid_row.append('.')
        else:
            grid_row.append(c)
    grid.append(grid_row)

# Directions: up, right, down, left
dirs = [(-1,0), (0,1), (1,0), (0,-1)]

def is_valid(pos):
    return 0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[0])

visited = set([start_pos])
pos = start_pos
direction = start_dir

while True:
    # Get next position
    next_pos = (pos[0] + dirs[direction][0], pos[1] + dirs[direction][1])
    
    # Check if we're still in bounds
    if not is_valid(next_pos):
        break
        
    # Check if obstacle ahead
    if grid[next_pos[0]][next_pos[1]] == '#':
        # Turn right
        direction = (direction + 1) % 4
    else:
        # Move forward
        pos = next_pos
        visited.add(pos)
        
print(len(visited))