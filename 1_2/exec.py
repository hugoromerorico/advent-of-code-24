data = [line.strip() for line in open("in.txt").readlines()]

arr1 = [int(d.split()[0]) for d in data]
dict2 = {}
for d in [int(d.split()[1]) for d in data]:
    dict2[d] = dict2.get(d, 0) + 1

sim = sum([n * dict2.get(n, 0) for n in arr1])

print(sim)