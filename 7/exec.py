def evaluate(nums, ops):
    result = nums[0]
    for i in range(len(ops)):
        if ops[i] == '+':
            result += nums[i+1]
        else:
            result *= nums[i+1]
    return result

def can_match(target, nums):
    if len(nums) == 1:
        return target == nums[0]
        
    def try_combinations(pos, curr_ops):
        if pos == len(nums)-1:
            return evaluate(nums, curr_ops) == target
        
        return (try_combinations(pos+1, curr_ops + ['+']) or 
                try_combinations(pos+1, curr_ops + ['*']))
                
    return try_combinations(0, [])

data = [line.strip() for line in open("in.txt") if line.strip()]

total = 0
for line in data:
    target, nums = line.split(': ')
    target = int(target)
    nums = [int(x) for x in nums.split()]
    
    if can_match(target, nums):
        total += target

print(total)