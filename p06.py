from .utils import *

def find_guard(grid):
    # find the initial coordinates of guard
    x = 0
    y = 0
    for y, row in enumerate(grid):
        try:
            x = row.index("^")
        except:
            continue

        break

    return (x,y)

def simulate(grid, p, d):
    # determine the maximum number of steps until we're in a loop
    m = len(grid[0])
    n = len(grid)
    max_steps = m*n

    # we'll count the steps
    steps = 0

    # move until we exit the grid
    
    while True:
        # mark the currrent position visited
        set_grid(grid, p, "X")
        
        # form the new position forward
        p1 = (p[0] + d[0], p[1] + d[1])

        # check if we have left the grid
        if not on_grid(grid,p1):
            return False # we walked off the grid

        # check if we have hit an obstacle
        if get_grid(grid,p1) == "#":
            # turn right
            d = (d[1], -d[0])
        else:
            # otherwise, step forward
            p = p1
            steps += 1
            if steps == max_steps:
                return True # in a loop

def compute_part1(grid):
    # initialize the position 
    p = find_guard(grid)

    # represent initial direction (up) with a vector
    d = (0,1)

    # move until we exit the grid
    loop = simulate(grid, p, d)
    assert(not loop)

    # count the number of visited positions
    count = 0
    for row in grid:
        for v in row:
            if v == "X":
                count += 1

    return count

Data1 = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

def get_grid_from_data(data):
    grid = data.splitlines()

    # internally, we use bottom left as origin
    grid.reverse()

    # make each row a list
    grid = [list(r) for r in grid]
    
    return grid

def get_test_data():
    return get_grid_from_data(Data1)

def get_full_data():
    with open(get_data_file("p06-data.txt")) as fp:
        data = fp.read()
    return get_grid_from_data(data)

def p06_part1():
    # run the tests
    grid = get_test_data()
    assert compute_part1(grid) == 41

    # compute the solution
    grid = get_full_data()
    return compute_part1(grid) 
    
def compute_part2(grid):
    # get the initial position and direction of guard
    p = find_guard(grid)
    d = (0,1)

    # try all unused positions to see if we can make a loop
    count = 0
    n = len(grid)
    m = len(grid[0])
    for y in range(n):
        for x in range(m):
            # ignore positions that are currently obstacles
            if get_grid(grid,(x,y)) == "#":
                continue

            # ignore the guard position
            if x == p[0] and y == [1]:
                continue

            # copy the grid
            grid2 = copy_grid(grid)

            # make the position an obstacle
            p2 = (x,y)
            set_grid(grid2, p2, "#")

            # run the simulation
            loop = simulate(grid2, p, d)

            # count the grid position if the guard went into a loop
            if loop:
                count += 1

    return count
    
def p06_part2():
    grid = get_full_data()
    return compute_part2(grid) 
    
__all__ = ["p06_part1", "p06_part2"]
