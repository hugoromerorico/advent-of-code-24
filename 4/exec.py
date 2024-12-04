def count_occurrences(string, pattern):
    count = 0
    for i in range(len(string) - len(pattern) + 1):
        if string[i:i+len(pattern)] == pattern:
            count += 1
        if string[i:i+len(pattern)] == pattern[::-1]:  # Check reversed pattern
            count += 1
    return count

def get_diagonals(data, rows, cols, forward=True):
    diagonals = []
    # Start from first row
    for col in range(cols):
        diagonal = ''
        r, c = 0, col
        while r < rows and (0 <= c < cols):
            diagonal += data[r][c]
            r += 1
            c = (c + 1) if forward else (c - 1)
        if len(diagonal) >= 4:
            diagonals.append(diagonal)
    
    # Start from first/last column
    for row in range(1, rows):
        diagonal = ''
        r, c = row, (0 if forward else cols-1)
        while r < rows and (0 <= c < cols):
            diagonal += data[r][c]
            r += 1
            c = (c + 1) if forward else (c - 1)
        if len(diagonal) >= 4:
            diagonals.append(diagonal)
    
    return diagonals

data = [line.strip() for line in open("in.txt").readlines() if line.strip()]

rows = len(data)
cols = len(data[0])
total = 0

# Horizontal
for row in data:
    total += count_occurrences(row, "XMAS")

# Vertical
for col in range(cols):
    vertical = ''.join(data[row][col] for row in range(rows))
    total += count_occurrences(vertical, "XMAS")

# Diagonal (top-left to bottom-right)
for diagonal in get_diagonals(data, rows, cols, True):
    total += count_occurrences(diagonal, "XMAS")

# Diagonal (top-right to bottom-left)
for diagonal in get_diagonals(data, rows, cols, False):
    total += count_occurrences(diagonal, "XMAS")

print(total)