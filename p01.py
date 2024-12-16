from .utils import *

def get_data():
    # load the data
    with open(get_data_file("p01-data.txt")) as fp:
        lines = fp.read().splitlines()
        pairs = [(int(l[0:5]), int(l[8:])) for l in lines]
    return pairs

def p01_part1():
    pairs = get_data()
    
    l1 = sorted([p[0] for p in pairs])
    l2 = sorted([p[1] for p in pairs])
    s = sum([abs(p[0] - p[1]) for p in zip(l1,l2)])
    return s

def p01_part2():
    pairs = get_data()
    
    # sort the left list
    l1 = sorted([p[0] for p in pairs])

    # extract the right list
    l2 = [p[1] for p in pairs]

    # determine the similarity score
    score = 0
    for n in l1:
        # how many times does this number appear in the right list?
        count = sum([1 if m == n else 0 for m in l2])
        # print(f"count: {count}")

        # aggregate score
        score += n*count

    return score

__all__ = ["p01_part1", "p01_part2"]
