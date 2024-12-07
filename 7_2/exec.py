data = [line.strip() for line in open("in.txt").readlines() if line.strip()]

def concat(a, b):
    return int(str(a) + str(b))

def evaluate(nums, ops):
    result = nums[0]
    for i in range(len(ops)):
        if ops[i] == '+':
            result += nums[i+1]
        elif ops[i] == '*':
            result *= nums[i+1]
        else:
            result = concat(result, nums[i+1])
    return result

def can_match(target, nums):
    if len(nums) == 1:
        return target == nums[0]
    
    operators = ['+', '*', '||']
    n = len(nums) - 1
    
    for op_combo in range(3**n):
        ops = []
        curr = op_combo
        for _ in range(n):
            ops.append(operators[curr % 3])
            curr //= 3
            
        if evaluate(nums, ops) == target:
            return True
            
    return False

total = 0
for line in data:
    target, nums = line.split(':')
    target = int(target)
    nums = [int(x) for x in nums.split()]
    
    if can_match(target, nums):
        total += target

print(total)