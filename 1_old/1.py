data = [line.strip() for line in open("in1.txt").readlines()]
# lines = open("in.txt").read().splitlines()

arr1 = sorted([d.split()[0] for d in data])a
arr2 = sorted([d.split()[1] for d in data])

dif = sum([abs(int(a) - int(b)) for a, b in zip(arr1, arr2)])

print(dif)
