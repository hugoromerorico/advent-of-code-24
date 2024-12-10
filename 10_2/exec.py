def count_paths(grid, start, height, memo):
    if height == 9:
        return 1
    
    state = (*start, height)
    if state in memo:
        return memo[state]
    
    paths = 0
    row, col = start
    for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
        new_row = row + dr
        new_col = col + dc
        
        if (0 <= new_row < len(grid) and 
            0 <= new_col < len(grid[0]) and
            grid[new_row][new_col] == height + 1):
            
            paths += count_paths(grid, (new_row, new_col), height + 1, memo)
    
    memo[state] = paths
    return paths

data = [line.strip() for line in open("in.txt") if line.strip()]
grid = [[int(c) for c in row] for row in data]

total = 0
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j] == 0:
            total += count_paths(grid, (i,j), 0, {})

print(total)