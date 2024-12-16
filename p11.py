from .utils import *

Stones1 = "125 17"
Stones2 = "965842 9159 3372473 311 0 6 86213 48"

def get_stones(data):
    data = data.split(" ")

    # we're working with numbers
    data = [int(x) for x in data]
    
    return data

def update(stones1):
    stones2 = []
    for s in stones1:
        # rule 1: 0 -> 1
        if s == 0:
            stones2.append(1)
            continue

        # rule 2: even length if digits are divided
        s_str = str(s)
        if len(s_str) % 2 == 0:
            m = len(s_str) // 2
            a = s_str[0:m]
            b = s_str[m:]
            stones2.append(int(a))
            stones2.append(int(b))
            continue

        # rule 3: multiply by 2024
        stones2.append(s*2024)

    return stones2

def blink(stones, n):
    for i in range(n):
        stones = update(stones)
    return stones

def stones_string(stones):
    return " ".join([str(s) for s in stones])

def part1(stones):
    stones = blink(stones, 25)
    return len(stones)

def p11_part1():
    # run the tests
    stones = get_stones(Stones1)
    assert part1(stones) == 55312

    # compute the solution
    stones = get_stones(Stones2)
    return part1(stones)
        
def blink_1(memo, s, depth):
    # check if we know the answer
    t = (s,depth)
    if t in memo:
        return memo[t]

    # evaluate one update for s
    stones = update([s])

    # check for the end condition
    if depth == 1:
        # memoize the result
        count = len(stones)
        memo[(s,1)] = count
        return count

    # recurse
    count = blink_n(memo, stones, depth-1)

    # memoize the result and return it
    memo[t] = count
    return count

def blink_n(memo, stones, depth):
    # aggregate results for each stone
    count = 0
    for s in stones:
        count += blink_1(memo, s, depth)
    return count
    
def p11_part2():
    # Map of tuple(a,d) -> b where b is the number of stones after d
    # blinks given stone a.
    memo = {}

    assert blink_n(memo,[125],1) == 1
    assert blink_n(memo,[125],2) == 2
    assert blink_n(memo,[125],3) == 2
    assert blink_n(memo,[125],4) == 3
    assert blink_n(memo,[125],5) == 5
    assert blink_n(memo,[125],6) == 7

    assert blink_n(memo,[17],1) == 2
    assert blink_n(memo,[17],2) == 2
    assert blink_n(memo,[17],3) == 3
    assert blink_n(memo,[17],4) == 6
    assert blink_n(memo,[17],5) == 8
    assert blink_n(memo,[17],6) == 15

    stones = get_stones(Stones2)
    return blink_n(memo, stones, 75)

__all__ = ["p11_part1", "p11_part2"]
