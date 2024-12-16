from .utils import *

Data1 = """AAAA
BBCD
BBCC
EEEC"""

Data2 = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""

Data3 = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
"""

Data4 = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""

Data5 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

def get_grid_from_data(data):
    data = data.splitlines()

    # make it a regular XY coordinate system
    data.reverse()

    return data

def get_full_data():
    with open(get_data_file("p12-data.txt")) as fp:
        data = fp.read()

    return get_grid_from_data(data)

#
# part1
#

def get_neighbours(p):
    x, y = p
    return [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]

def get_region(grid, visited, p0):
    # get the name/type of the region
    name = get_grid(grid, p0)

    # list of points belonging to the region
    points = []

    # search over the grid starting at p0
    queue = [p0]
    while len(queue) > 0:
        # deque the next point
        p = queue.pop()

        # ignore it if it was visited
        if p in visited:
            continue

        # mark it visited
        visited[p] = True

        # add it to the region
        points.append(p)

        # visit neighbours
        neighbours = get_neighbours(p)
        for n in neighbours:
            # ignore points not on the grid
            if not on_grid(grid, n):
                continue

            # ignore points already visited
            if n in visited:
                continue

            # ignore points with different region name
            name2 = get_grid(grid, n)
            if name != name2:
                continue

            # enqueue this point
            queue.append(n)

    return points

def get_regions(grid):
    # map of coord -> bool for visited coordinates
    visited = {}

    # visit all the grid points to determine regions
    regions = []
    for y, row in enumerate(grid):
        for x, region in enumerate(row):
            p = (x,y)
            if p not in visited:
                region = get_region(grid, visited, p)
                regions.append(region)

    return regions

def get_region_perimeter(grid, region):
    # we'll accumulate the perimeter
    perim = 0

    # get the name/type of the region
    name = get_grid(grid, region[0])

    # check each point in the region and its neighbours
    for p in region:
        neighbours = get_neighbours(p)
        for n in neighbours:
            # if it's outside the grid, we need a fence
            if not on_grid(grid, n):
                perim += 1
                continue

            # if it is not the same region type, we need a fence
            name2 = get_grid(grid, n)
            if name != name2:
                perim += 1
                continue

    return perim

def compute_part1(grid):
    # get the regions
    regions = get_regions(grid)

    # compute the cost
    cost = 0
    for r in regions:
        area = len(r)
        perim = get_region_perimeter(grid, r)
        cost += area*perim
    return cost

def p12_part1():
    # run the tests
    grid = get_grid_from_data(Data1)
    assert compute_part1(grid) == 140
    grid = get_grid_from_data(Data2)
    assert compute_part1(grid) == 772

    # compute the solution
    grid = get_full_data()
    return compute_part1(grid)

#
# part2
#

Corners = [
    # convex corners
    {
        "in": None,
        "out": [(0, 1), (-1, 0)],
    },
    {
        "in": None,
        "out": [(-1, 0), (0, -1)],
    },
    {
        "in": None,
        "out": [(0, -1), (1, 0)],
    },
    {
        "in": None,
        "out": [(1, 0), (0, 1)],
    },

    # concave corners
    {
        "in": [(0, 1), (-1, 0)],
        "out": [(-1, 1)],
    },
    {
        "in": [(-1, 0), (0, -1)],
        "out": [(-1, -1)],
    },
    {
        "in": [(1, 0), (0, -1)],
        "out": [(1, -1)],
    },
    {
        "in": [(1, 0), (0, 1)],
        "out": [(1, 1)],
    },
]
    
def is_corner(rmap, p, c):
    # check that specified points are in
    if c["in"]:
        points = [v2_plus(p, d) for d in c["in"]]
        points_in = [p in rmap for p in points]
        if not all(points_in):
            return False

    # check that specified points are out
    if c["out"]:
        points = [v2_plus(p, d) for d in c["out"]]
        points_out = [p not in rmap for p in points]
        if not all(points_out):
            return False

    return True
    
def count_corners(region):
    # create the region map
    rmap = {p: True for p in region}
    
    # count all the corners
    count = 0
    for p in rmap:
        for c in Corners:
            if is_corner(rmap, p, c):
                count += 1

    return count

def compute_cost(grid):
    # get the regions
    regions = get_regions(grid)

    # compute the cost
    total = 0
    for region in regions:
        name = get_grid(grid, region[0])
        area = len(region)
        corners = count_corners(region)
        cost = area*corners
        total += cost

    return total

def p12_part2():
    # run the tests
    grid = get_grid_from_data(Data1)
    assert compute_cost(grid) == 80
    
    grid = get_grid_from_data(Data2)
    assert compute_cost(grid) == 436

    grid = get_grid_from_data(Data3)
    assert compute_cost(grid) == 236

    grid = get_grid_from_data(Data4)
    assert compute_cost(grid) == 368

    grid = get_grid_from_data(Data5)
    assert compute_cost(grid) == 1206
    
    # compute the solution
    grid = get_full_data()
    return compute_cost(grid)
    
__all__ = ["p12_part1", "p12_part2"]
