data = [line.strip() for line in open("in.txt").readlines()]

arr1 = sorted([int(d.split()[0]) for d in data])
arr2 = sorted([int(d.split()[1]) for d in data])

total = 0
for a, b in zip(arr1, arr2):
    total += abs(a - b)

print(total)