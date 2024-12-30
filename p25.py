from .utils import *

Data1 = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""

def can_fit(key, lock):
    return all([a + b <= 7 for a, b in zip(key,lock)])

def parse_item(lines):
    is_key = lines[0][0] == "."
    item = [0]*5
    for i in range(5):
        col = [1 if line[i] == "#" else 0 for line in lines]
        item[i] = sum(col)
    return item, is_key

def solve1(data):
    # convert to lines
    lines = data.splitlines()

    # read the items
    keys = []
    locks = []
    i = 0
    while i < len(lines):
        # parse the item
        item, is_key = parse_item(lines[i:i+7])
        if is_key:
            keys.append(item)
        else:
            locks.append(item)

        # skip the newline
        i += 8

    count = 0
    for key in keys:
        for lock in locks:
            if can_fit(key,lock):
                count += 1
    return count

def p25_part1():
    # run the tests
    count = solve1(Data1)
    assert count == 3

    # compute the solution
    with open(get_data_file("p25-data.txt")) as fp:
        data = fp.read()
    count = solve1(data)
    return count

def p25_part2():
    # there is no second part!
    return 0

__all__ = ["p25_part1", "p25_part2"]
