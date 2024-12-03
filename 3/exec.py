import re

data = open("in.txt").read().strip()

total = 0
for match in re.finditer(r'mul\((\d+),(\d+)\)', data):
    n1 = int(match.group(1))
    n2 = int(match.group(2)) 
    total += n1 * n2

print(total)