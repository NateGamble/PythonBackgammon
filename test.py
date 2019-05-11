import random

a = [1,2,3,4,5,1]
a[a.index(1)] = .5
print(a)

enum = [i for i,x in enumerate([1,2,3,2,2,2,2]) if x==2]
print(enum)

lst = [1,1,2]
lst.remove(1)
print(lst)

print(bool(0))

black_roll = [1,2]
roll_idx = random.randint(0, len(black_roll) - 1)
print(roll_idx)