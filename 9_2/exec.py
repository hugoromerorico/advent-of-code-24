data = open("in.txt").read().strip()

# Parse the disk map into blocks and track file sizes
nums = [int(x) for x in data]
blocks = []
file_sizes = {}
file_id = 0
for i in range(0, len(nums), 2):
    size = nums[i]
    file_sizes[file_id] = size
    for _ in range(size):
        blocks.append(file_id)
    file_id += 1
    if i+1 < len(nums):
        blocks.extend([-1] * nums[i+1])

# Process files in decreasing ID order
for current_id in range(max(file_sizes.keys()), -1, -1):
    if current_id not in file_sizes:
        continue
        
    size = file_sizes[current_id]
    
    # Find file start position
    file_start = -1
    for i in range(len(blocks)):
        if blocks[i] == current_id:
            file_start = i
            break
            
    # Find leftmost valid position
    best_pos = -1
    space_count = 0
    for i in range(len(blocks)):
        if blocks[i] == -1:
            space_count += 1
            if space_count >= size:
                best_pos = i - size + 1
                break
        else:
            space_count = 0
            
    if best_pos != -1 and best_pos < file_start:
        # Clear old position
        for i in range(file_start, file_start + size):
            blocks[i] = -1
            
        # Place in new position
        for i in range(best_pos, best_pos + size):
            blocks[i] = current_id

checksum = sum(pos * id for pos, id in enumerate(blocks) if id != -1)
print(checksum)