data = [line.strip() for line in open("in.txt").readlines() if line.strip()]
width = len(data[0])
height = len(data)

def check_xmas(r, c):
    # Check X shape with MAS forwards or backwards at each end
    patterns = [
        [('M','A','S'), ('M','A','S')],  # Both forward
        [('S','A','M'), ('M','A','S')],  # First backwards, second forwards 
        [('M','A','S'), ('S','A','M')],  # First forwards, second backwards
        [('S','A','M'), ('S','A','M')]   # Both backwards
    ]
    
    if r + 2 >= height or c + 2 >= width:
        return False
        
    for p in patterns:
        # Left diagonal
        if (data[r][c] == p[0][0] and
            data[r+1][c+1] == p[0][1] and  
            data[r+2][c+2] == p[0][2] and
            # Right diagonal 
            data[r][c+2] == p[1][0] and
            data[r+1][c+1] == p[1][1] and
            data[r+2][c] == p[1][2]):
            return True
            
    return False

count = 0
for r in range(height):
    for c in range(width):
        if check_xmas(r, c):
            count += 1

print(count)