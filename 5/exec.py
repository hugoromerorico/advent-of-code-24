def parse_input():
    rules = set()
    updates = []
    reading_rules = True
    
    for line in open("in.txt"):
        line = line.strip()
        if not line:
            continue
            
        if ',' in line:
            reading_rules = False
            updates.append([int(x) for x in line.split(',')])
        elif reading_rules:
            if '|' in line:
                a, b = map(int, line.split('|'))
                rules.add((a, b))
                
    return rules, updates

def is_valid_order(pages, rules):
    seen = set()
    for page in pages:
        seen.add(page)
        
        # Check if any rule is violated
        for before, after in rules:
            if before in seen and after in seen:
                if pages.index(after) < pages.index(before):
                    return False
                    
    return True

rules, updates = parse_input()
total = 0

for update in updates:
    if is_valid_order(update, rules):
        middle_idx = len(update) // 2
        total += update[middle_idx]
        
print(total)