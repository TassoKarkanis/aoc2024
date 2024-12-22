from .utils import *

Data1 = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""

class Solver:
    def __init__(self, data):
        self.grid = None   # grid containing the map and path
        self.path = []     # list of positions from S to E inclusive
        self.dist = {}     # map of pos on path -> distance to E
        self.cheats = []   # list of tuples (p1, p2)
        self.savings = {}  # map of distance saved -> count of cheats
        
        # parse the data
        lines = data.splitlines()
        self.grid = [row for row in lines]

    def solve(self, cheat_dist):
        self.find_path()
        self.compute_dist()
        self.find_cheats(cheat_dist)
        self.get_savings()
        
    def find_path(self):
        grid = self.grid
        
        # find the start and end points
        for y, row in enumerate(grid):
            for x, val in enumerate(row):
                if val == "S":
                    start = (x, y)
                elif val == "E":
                    end = (x, y)
    
        # walk the path
        p = start
        path = [p]
        at_end = False
        while not at_end:
            x, y = p
            for p1 in ((x+1, y), (x, y+1), (x-1, y), (x, y-1)):
                # ignore off-grid positions
                if not on_grid(grid, p1):
                    continue
    
                # ignore the previous position
                if len(path) >= 2 and p1 == path[-2]:
                    continue
    
                # check the value
                val = get_grid(grid, p1)
                if val == "#":
                    continue
                
                at_end = val == "E"
                p = p1
                path.append(p)
                break
        
        self.path = path

    def compute_dist(self):
        # return a map of point -> distance to end
        dist = {}
        for i, p in enumerate(reversed(self.path)):
            dist[p] = i
        self.dist = dist

    def find_cheats(self, cheat_dist):
        grid = self.grid
        cheats = []

        # A cheat distance induces a diamond-shaped region centered on
        # the each position of the path.  Any point in that diamond is
        # reachable within a number of steps (the cheat distance).
        
        for y, row in enumerate(grid):
            for x, val in enumerate(row):
                # ignore invalid positions
                if val not in ("S", "."):
                    continue

                # point around which diamond shape is centered
                p0 = (x, y)

                # iterate over all points in the diamond shape
                for j in range(-cheat_dist, cheat_dist + 1):
                    m = cheat_dist - abs(j)
                    for i in range(-m, m + 1):
                        # ignore the current point
                        if i == 0 and j == 0:
                            continue

                        # compute the resulting cheat point
                        p1 = (x + i, y + j)

                        # check that the cheat point is on the grid
                        if not on_grid(grid, p1):
                            continue

                        # check that it is on the path
                        val = get_grid(grid, p1)
                        if val not in (".", "E"):
                            continue

                        # add the cheat
                        cheats.append((p0, p1))
    
        self.cheats = cheats

    def get_savings(self):
        path = self.path
        dist = self.dist
        cheats = self.cheats
        
        # map of saving to count of cheats
        savings = {}
        total_len = dist[path[0]]
        for cheat in cheats:
            p0 = cheat[0]
            p1 = cheat[1]
            
            d1 = dist[p0]
            d2 = dist[p1]
            if d2 >= d1:
                continue

            # compute the distance between the cheat positions
            d3 = abs(p0[0] - p1[0]) + abs(p0[1] - p1[1])
            
            d = d1 - (d2 + d3)
            if d not in savings:
                savings[d] = 0
            savings[d] += 1

        self.savings = savings

def get_full_data():
    with open(get_data_file("p20-data.txt")) as fp:
        data = fp.read()
    return data

def count_cheats(savings, cutoff):
    counts = 0
    for saving, count in savings.items():
        if saving >= cutoff:
            counts += count
    return counts

def p20_part1():
    # run the tests
    s = Solver(Data1)
    s.solve(2)
    assert s.dist[s.path[0]] == 84
    assert s.savings[2] == 14
    assert s.savings[4] == 14
    assert s.savings[6] == 2
    assert s.savings[8] == 4
    assert s.savings[10] == 2
    assert s.savings[12] == 3

    # compute the solution
    s = Solver(get_full_data())
    s.solve(2)
    counts = count_cheats(s.savings, 100)
    return counts
    
def p20_part2():
    s = Solver(Data1)
    s.solve(20)
    test_data = ((50, 32),
                 (52, 31),
                 (54, 29),
                 (56, 39),
                 (58, 25),
                 (60, 23),
                 (62, 20),
                 (64, 19),
                 (66, 12),
                 (68, 14),
                 (70, 12),
                 (72, 22),
                 (74, 4 ),
                 (76, 3 ))
    for d in test_data:
        assert s.savings[d[0]] == d[1]

    # compute the solution
    s = Solver(get_full_data())
    s.solve(20)
    counts = count_cheats(s.savings, 100)
    return counts
    
__all__ = ["p20_part1", "p20_part2"]
