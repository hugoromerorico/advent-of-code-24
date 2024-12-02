data = [line.strip() for line in open("in.txt").readlines()]

arr1 = sorted([int(d.split()[0]) for d in data])
arr2 = sorted([int(d.split()[1]) for d in data])

total = sum(abs(a - b) for a, b in zip(arr1, arr2))
print(total)