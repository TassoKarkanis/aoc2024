import bisect

from .utils import *

Data1 = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

def draw_grid(grid):
    for row in grid:
        print("".join(row))

def get_points(data):
    lines = data.splitlines()
    points = [l.split(",") for l in lines]
    points = [(int(p[0]), int(p[1])) for p in points]
    return points

def get_grid(points, m, n, k):
    # make the grid
    grid = [list("."*m) for i in range(n)]
    for p in points[0:k]:
        set_grid(grid, p, "#")

    return grid

def make_graph(grid):
    V = set()
    E = {}
    EC = {}

    # helper function
    def add_edge(v1, v2):
        # add the vertices
        V.add(v1)
        V.add(v2)

        # add the edge
        neighbours = None
        if v1 in E:
            neighbours = E[v1]
        else:
            neighbours = set()
            E[v1] = neighbours
        neighbours.add(v2)

        # add the edge cost
        e = (v1, v2)
        EC[e] = 1

    # build the graph
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val != ".":
                continue
            
            neighbours = [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]
            p1 = (x, y)
            for p2 in neighbours:
                if on_grid(grid, p2):
                    add_edge(p1, p2)

    G = (V, E, EC)
    return G

def solve1(data, m, n, k):
    # get the points, grid, and graph
    points = get_points(data)
    grid = get_grid(points, m, n, k)
    # draw_grid(grid)
    g = make_graph(grid)

    # run Dijkstra
    source = (0, 0)
    dist, prev = dijkstra(g, source)

    # get the shortest path to the target
    target = (m-1, n-1)
    path = shortest_path(source, target, dist, prev)
    steps = len(path) - 1
    return steps

def test1():
    steps = solve1(Data1, 7, 7, 12)
    assert steps == 22

def get_full_data():
    with open(get_data_file("p18-data.txt")) as fp:
        data = fp.read()
    return data
    
def p18_part1():
    # run the tests
    test1()

    # compute the solution
    steps = solve1(get_full_data(), 71, 71, 1024)
    return steps

def solve2(data, m, n):
    # get the points
    points = get_points(data)

    def check_path(k):
        grid = get_grid(points, m, n, k)
        g = make_graph(grid)
        
        # run Dijkstra
        source = (0, 0)
        dist, prev = dijkstra(g, source)
        
        # get the shortest path to the target
        target = (m-1, n-1)
        path = shortest_path(source, target, dist, prev)
        return 0 if len(path) > 0 else 1

    # binary search for the index in points
    k = bisect.bisect_left(range(len(points)), 1, key=check_path)

    # form the output string
    p = points[k-1]
    return ",".join(map(str,p))
    
def test2():
    s = solve2(Data1, 7, 7)
    assert s == "6,1"

def p18_part2():
    # run the tests
    test2()

    # compute the solution
    s = solve2(get_full_data(), 71, 71)
    return s
    
__all__ = ["p18_part1", "p18_part2"]
