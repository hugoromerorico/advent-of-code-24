def get_rules(rules):
    graph = {}
    for rule in rules:
        if '|' not in rule:
            continue
        a, b = map(int, rule.split('|'))
        if a not in graph:
            graph[a] = set()
        graph[a].add(b)
    return graph

def is_valid_order(nums, graph):
    seen = set()
    for n in nums:
        seen.add(n)
        if n in graph:
            for must_be_after in graph[n]:
                if must_be_after in seen:
                    return False
    return True

def get_valid_order(nums, graph):
    nums = list(nums)
    changed = True
    while changed:
        changed = False
        for i in range(len(nums)-1):
            a = nums[i]
            b = nums[i+1]
            if a in graph and b in graph[a]:
                nums[i], nums[i+1] = nums[i+1], nums[i]
                changed = True
    return nums

data = open("in.txt").read().strip().split('\n')

rules = []
updates = []
in_rules = True
for line in data:
    if not line:
        in_rules = False
        continue
    if in_rules:
        rules.append(line)
    else:
        updates.append([int(x) for x in line.split(',')])

graph = get_rules(rules)

total = 0
for update in updates:
    if not is_valid_order(update, graph):
        valid_order = get_valid_order(update, graph)
        total += valid_order[len(valid_order)//2]

print(total)