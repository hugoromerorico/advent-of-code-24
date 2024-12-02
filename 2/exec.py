data = [line.strip() for line in open("in.txt").readlines()]

def is_safe(nums):
    diffs = [nums[i+1] - nums[i] for i in range(len(nums)-1)]
    
    # Check if all differences are between 1-3 or -(1-3)
    if not all(1 <= abs(d) <= 3 for d in diffs):
        return False
        
    # Check if all increasing or all decreasing
    if not (all(d > 0 for d in diffs) or all(d < 0 for d in diffs)):
        return False
        
    return True

safe_count = 0
for line in data:
    nums = [int(x) for x in line.split()]
    if is_safe(nums):
        safe_count += 1
        
print(safe_count)