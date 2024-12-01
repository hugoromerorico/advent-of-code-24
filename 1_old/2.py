data = [line.strip() for line in open("in1.txt").readlines()]

arr1 = [int(d.split()[0]) for d in data]
dic2 = {}
for d in [int(d.split()[1]) for d in data]:
    dic2[d] = dic2.get(d, 0) + 1

sim = sum([d1 * dic2.get(d1, 0) for d1 in arr1])

print(sim)
