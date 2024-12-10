def find_paths(grid, start, visited, height):
    if height == 9:
        return {tuple(start)}
    
    paths = set()
    row, col = start
    for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
        new_row = row + dr
        new_col = col + dc
        
        if (0 <= new_row < len(grid) and 
            0 <= new_col < len(grid[0]) and
            (new_row, new_col) not in visited and
            grid[new_row][new_col] == height + 1):
            
            visited.add((new_row, new_col))
            paths.update(find_paths(grid, [new_row, new_col], visited, height + 1))
            visited.remove((new_row, new_col))
            
    return paths

data = [line.strip() for line in open("in.txt") if line.strip()]
grid = [[int(c) for c in row] for row in data]

total = 0
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j] == 0:
            paths = find_paths(grid, [i,j], {(i,j)}, 0)
            total += len(paths)

print(total)