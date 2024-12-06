def get_path(grid, x, y, direction, blocked):
    height = len(grid)
    width = len(grid[0])
    visited = []
    pos = (x, y)
    
    dirs = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
    turns = {'^': '>', '>': 'v', 'v': '<', '<': '^'}
    
    loop_found = False
    seen = set()
    
    while True:
        current_state = (pos, direction)
        if current_state in seen:
            loop_found = True
            break
        seen.add(current_state)
        visited.append(pos)
            
        dx, dy = dirs[direction]
        next_x = pos[0] + dx
        next_y = pos[1] + dy
        next_pos = (next_x, next_y)
        
        if next_x < 0 or next_x >= height or next_y < 0 or next_y >= width:
            break
        
        if next_pos in blocked or grid[next_x][next_y] == '#':
            direction = turns[direction] 
        else:
            pos = next_pos
            
    return visited, loop_found

def find_loops(grid):
    height = len(grid)
    width = len(grid[0])
    
    # Find the starting position and direction
    start_x = start_y = None
    start_direction = None
    for i in range(height):
        for j in range(width):
            if grid[i][j] in '^>v<':
                start_direction = grid[i][j]
                start_x, start_y = i, j
                break
        if start_direction:
            break
    
    if start_x is None or start_direction is None:
        raise ValueError("Starting position with direction not found in the grid.")
    
    loop_positions = 0
    for x in range(height):
        for y in range(width):
            if (x == start_x and y == start_y) or grid[x][y] != '.':
                continue
            
            # Place obstruction at (x, y)
            blocked = {(x, y)}
            _, has_loop = get_path(grid, start_x, start_y, start_direction, blocked)
            if has_loop:
                loop_positions += 1
                
    return loop_positions

if __name__ == "__main__":
    grid = [list(line.strip()) for line in open('in.txt').readlines() if line.strip()]
    print(find_loops(grid))