data = open("in.txt").read().strip()

# Parse input into numbers
numbers = [int(c) for c in data]

# Build initial disk map
disk = []
file_id = 0
for i in range(0, len(numbers)):
    if i % 2 == 0:  # File blocks
        disk.extend([file_id] * numbers[i])
        file_id += 1
    else:  # Free space
        disk.extend([-1] * numbers[i])  # Use -1 for free space

# Compact files by moving rightmost files into leftmost spaces
while True:
    # Find leftmost free space
    space_pos = -1
    for i in range(len(disk)):
        if disk[i] == -1:
            space_pos = i
            break
            
    if space_pos == -1:
        break
        
    # Find rightmost file block after the free space
    file_pos = -1
    for i in range(len(disk)-1, space_pos, -1):
        if disk[i] != -1:
            file_pos = i
            break
            
    if file_pos == -1:
        break
        
    # Move the file block
    disk[space_pos] = disk[file_pos]
    disk[file_pos] = -1

# Calculate checksum
checksum = 0
for pos, block in enumerate(disk):
    if block != -1:
        checksum += pos * block

print(checksum)