def is_safe(nums):
    if len(nums) < 2:
        return True
        
    diff = nums[1] - nums[0]
    if abs(diff) > 3 or abs(diff) < 1:
        return False
    
    increasing = diff > 0
    
    for i in range(1, len(nums)-1):
        curr_diff = nums[i+1] - nums[i]
        if abs(curr_diff) > 3 or abs(curr_diff) < 1:
            return False
        if (curr_diff > 0) != increasing:
            return False
            
    return True

data = [line.strip() for line in open("in.txt").readlines()]
nums_list = [[int(x) for x in line.split()] for line in data]

safe = 0
for nums in nums_list:
    if is_safe(nums):
        safe += 1
        continue
        
    for i in range(len(nums)):
        test = nums[:i] + nums[i+1:]
        if is_safe(test):
            safe += 1
            break
            
print(safe)