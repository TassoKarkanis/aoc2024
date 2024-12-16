from .utils import *

Data1 = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

def is_safe(l):
    # get all but the last item
    l1 = list(l)[0:len(l)-1]

    # get all but the first item
    l2 = list(l)[1:]

    # form the pairwise differences
    l3 = [p[0] - p[1] for p in zip(l1,l2)]

    # check that they are increasing or decreasing
    if not (all([p < 0 for p in l3]) or all([p > 0 for p in l3])):
        return False

    # check that they differ by at most 3
    if not all([abs(p) <= 3 for p in l3]):
        return False

    # this level is safe
    return True

def count_safe(data, part2):
    # count the safe levels
    safe = 0
    for l in data:
        if is_safe(l):
            safe += 1
            continue

        if part2:
            # form all sub-lists and check them
            for i in range(len(l)):
                l2 = list(l)
                l2.pop(i)
                if is_safe(l2):
                    safe += 1
                    break

    return safe

def get_data(raw):
    data = raw.splitlines()
    data = [[int(n) for n in line.split(" ")] for line in data]
    return data

def get_full_data():
    with open(get_data_file("p02-data.txt")) as fp:
        return get_data(fp.read())

def p02_part1():
    # run the tests
    data = get_data(Data1)
    assert count_safe(data,False) == 2

    # compute solution
    data = get_full_data()
    return count_safe(data, False)

def p02_part2():
    # run the tests
    data = get_data(Data1)
    assert count_safe(data,True) == 4

    # compute solution
    data = get_full_data()
    return count_safe(data, True)


__all__ = ["p02_part1", "p02_part2"]

