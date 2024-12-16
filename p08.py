from .utils import *

Nodes = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

def get_grid_from_data(data):
    grid = data.splitlines()
    
    # internally, we use bottom left as origin
    grid.reverse()

    # make each row a list
    grid = [list(r) for r in grid]
    
    return grid

def get_full_data():
    with open(get_data_file("p08-data.txt")) as fp:
        data = fp.read()
    return get_grid_from_data(data)

def get_test_data():
    return get_grid_from_data(Nodes)

def get_antennas(grid):
    # determine all the antenna locations by type
    antennas = {}
    for x, row in enumerate(grid):
        for y, v in enumerate(row):
            if v != ".":
                points = []
                if v in antennas:
                    points = antennas[v]
                points.append((x,y))
                antennas[v] = points
    return antennas

def compute_part1(grid):
    antennas = get_antennas(grid)

    # compute the antinodes
    antinodes = {}
    for _, points in antennas.items():
        for i in range(len(points)):
            for j in range(i+1, len(points)):
                # compute the vector (p1 - p0)
                p0 = points[i]
                p1 = points[j]
                d = v2_minus(p1, p0)

                # compute the antinode locations
                q0 = v2_minus(p0, d)
                q1 = v2_plus(p1, d)

                # add them if they are on the grid
                if on_grid(grid,q0):
                    antinodes[q0] = True
                if on_grid(grid,q1):
                    antinodes[q1] = True

    return len(antinodes)

def p08_part1():
    # run the tests
    grid = get_test_data()
    assert compute_part1(grid) == 14

    # compute the solution
    grid = get_full_data()
    return compute_part1(grid)
    
def compute_part2(grid):
    antennas = get_antennas(grid)

    # compute the antinodes
    antinodes = {}
    for _, points in antennas.items():
        for i in range(len(points)):
            for j in range(i+1, len(points)):
                p0 = points[i]
                p1 = points[j]
                
                # compute the vector (p1 - p0)
                d = v2_minus(p1, p0)

                # compute the antinode locations at and behind p0
                k = 0
                while True:
                    d2 = v2_mult(k, d)
                    p = v2_minus(p0, d2)
                    if not on_grid(grid, p):
                        break

                    antinodes[p] = True
                    k += 1


                # compute the antinode locations at and in front of p1
                k = 0
                while True:
                    d2 = v2_mult(k, d)
                    p = v2_plus(p1, d2)
                    if not on_grid(grid, p):
                        break

                    antinodes[p] = True
                    k += 1

    return len(antinodes)

def p08_part2():
    # run the tests
    grid = get_test_data()
    assert compute_part2(grid) == 34

    # compute the solution
    grid = get_full_data()
    return compute_part2(grid)
    
__all__ = ["p08_part1", "p08_part2"]
