from .utils import *

Data1 = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

def get_data(topo_map):
    grid = topo_map.splitlines()

    # convert to numbers
    grid = [[int(x) for x in row] for row in grid]
    
    # fix the coordinate system
    grid.reverse()
    
    return grid

def get_test_data():
    return get_data(Data1)

def get_full_data():
    with open(get_data_file("p10-data.txt")) as fp:
        data = fp.read()
    return get_data(data)

#
# parts
#

def find_trail_heads(grid):
    trail_heads = []
    for y, row in enumerate(grid):
        for x, v in enumerate(row):
            if v == 0:
                trail_heads.append((x,y))
    return trail_heads
    

def trail_head_score(grid, p0):
    # Implement depth-first search to climb the hills.

    # positions that are visited
    visited = {}

    # all positions at the top of a trail (with value 9)
    goals = {}

    # positions remaining to visit
    queue = [p0]

    while len(queue) > 0:
        # dequeue the next position
        p = queue.pop()

        # ignore it if has been visited
        if p in visited:
            continue

        # now it has been visited
        visited[p] = True

        # is it a goal?
        v = get_grid(grid, p)
        if v == 9:
            # add it to the goals
            goals[p] = True
            continue

        # enqueue the appropriate neighbours
        x, y = p
        neighbours = [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]
        for q in neighbours:
            # ignore invalid ones
            if not on_grid(grid, q):
                continue
            
            # ignore ones that have already been visited
            if q in visited:
                continue

            # ignore ones that don't represent a step up
            v2 = get_grid(grid, q)
            if v2 != v+1:
                continue

            # we've got a live one here!
            queue.append(q)

    # all done
    return len(goals)

def part1(grid):
    # find all the trail heads
    trail_heads = find_trail_heads(grid)

    # compute the sum of trail head scores
    scores = 0
    for p in trail_heads:
        s = trail_head_score(grid, p)
        scores += s

    return scores

def p10_part1():
    # run the tests
    grid = get_test_data()
    assert part1(grid) == 36

    # compute the solution
    grid = get_full_data()
    return part1(grid)


def trail_head_rating(grid, p0):
    # Implement depth-first search to climb the hills.

    # count of the number of times a 9 is reached
    count = 0

    # positions remaining to visit
    queue = [p0]

    while len(queue) > 0:
        # dequeue the next position
        p = queue.pop()

        # is it a goal?
        v = get_grid(grid, p)
        if v == 9:
            # add a goal
            count += 1
            continue

        # enqueue the appropriate neighbours
        x, y = p
        neighbours = [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]
        for q in neighbours:
            # ignore invalid ones
            if not on_grid(grid, q):
                continue
            
            # ignore ones that don't represent a step up
            v2 = get_grid(grid, q)
            if v2 != v+1:
                continue

            # we've got a live one here!
            queue.append(q)

    # all done
    return count
    
def part2(grid):
    # find all the trail heads
    trail_heads = find_trail_heads(grid)

    # compute the sum of trail head ratings
    ratings = 0
    for p in trail_heads:
        s = trail_head_rating(grid, p)
        ratings += s

    return ratings

def p10_part2():
    # run the tests
    grid = get_test_data()
    assert part2(grid) == 81

    # compute the solution
    grid = get_full_data()
    return part2(grid)
    
__all__ = ["p10_part1", "p10_part2"]
