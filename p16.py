import heapq
import sys

from .utils import *

Data1 = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""


Data2 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""
        
Compass = ("N", "E", "S", "W")  # direction constants

def shortest_path_vertices(source, target, dist, prev):
    visited = set()

    # check that there is a path to the target
    if target not in prev:
        return visited

    Q = set([target])
    while len(Q) > 0:
        # dequeue a vertex
        v = Q.pop()

        # check that we haven't seen it already
        if v in visited:
            continue

        # add it to our set
        visited.add(v)

        # terminate at the source
        if v == source:
            continue

        # arrange to visit the predecessors
        Q |= prev[v]

    return visited
    
class Maze:
    def __init__(self, data):
        # parse the grid
        lines = data.splitlines()
        self.grid = [[c for c in line] for line in lines]
        self.m = len(self.grid[0])
        self.n = len(self.grid)
        
    def solve(self):
        # find the source and target points
        source_p = self.find_cell("S")
        target_p = self.find_cell("E")

        # make the graph
        G = self.make_graph()

        # apply Djikstra's algorithm
        source = (source_p, "E")
        dist, prev = dijkstra(G, source)

        # find the shortest path
        min_dist = sys.maxsize
        min_path = None
        for d in ("N", "E", "S", "W"):
            target = (target_p, d)
            path = shortest_path(source, target, dist, prev)
            if len(path) == 0:
                continue
            path_dist = dist[path[-1]]
            if path_dist < min_dist:
                min_dist = path_dist
                min_path = path

        return min_path, min_dist

    def solve2(self):
        # find the source and target points
        source_p = self.find_cell("S")
        target_p = self.find_cell("E")

        # make the graph
        G = self.make_graph()

        # apply Djikstra's algorithm
        source = (source_p, "E")
        dist, prev = dijkstra(G, source)

        # get all points on shortest paths
        points = None
        min_dist = sys.maxsize
        for d in Compass:
            target = (target_p, d)

            # determine if we should use these paths
            reset = dist[target] < min_dist
            merge = dist[target] == min_dist

            if not (reset or merge):
                continue
            
            # compute the vertices on the shortest path(s)
            verts = shortest_path_vertices(source, target, dist, prev)

            if reset:
                points = set()
                min_dist = dist[target]

            points |= set([v[0] for v in verts])

        return points

    def find_cell(self, val):
        p = None
        for y, row in enumerate(self.grid):
            try:
                x = row.index(val)
                p = (x, y)
                break
            except:
                pass
        return p

    def make_graph(self):
        # Make the corresponding graph.  The graph is represented as:
        #
        #   G = (V, E, EC)
        #
        # where:
        #
        #   V: Vertices of the graph are of the form (p,d) where p is
        #      a tuple (x,y) and d is one of ("N", "E", "S", "W") and
        #      represents the direction in which the reindeer is
        #      facing.
        #
        #   E: edges as a map of v vertex to set of vertices
        #
        #   EC: cost of edges as map of (v1,v2) -> cost

        V = set()
        E = {}
        EC = {}

        # a helper function to build the graph structure
        def add_edge(v1, v2, cost):
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
            EC[e] = cost

        W1 = 1  # weight of edge representing a forward move
        W2 = 1000 # weight of edge representing a turn
        
        for y, row in enumerate(self.grid):
            for x, val in enumerate(row):
                # check if this position is valid
                if val == "#":
                    continue

                # form the adjacent positions of the compass points
                adj = [(x, y-1), (x+1, y), (x, y+1), (x-1, y)]

                # determine if they are valid
                valid = list(map(lambda p: get_grid(self.grid,p) != "#", adj))

                # account for forward movements from this position
                p1 = (x, y)
                for i in range(4):
                    if valid[i]:
                        d = Compass[i]
                        v1 = (p1, d)
                        v2 = (adj[i], d)
                        add_edge(v1, v2, W1)

                # Account for turns at this position.  We only add
                # these vertices/edges as necessary.
                for i in range(4):
                    if valid[i]:
                        v2 = (p1, Compass[i])
                        v1 = (p1, Compass[(i+1) % 4])
                        add_edge(v1, v2, W2)

                        v1 = (p1, Compass[(i+3) % 4])
                        add_edge(v1, v2, W2)

        # return the graph
        G = (V, E, EC)
        return G

def draw_maze(grid, path):
    # copy the grid
    grid = [row.copy() for row in grid]

    # arrows for the directions positions
    arrows = {
        "N": "^",
        "E": ">",
        "S": "v",
        "W": "<",
    }

    # overwrite with the paths
    for v in path[1:len(path)-1]:
        set_grid(grid, v[0], arrows[v[1]])

    # print it out
    for row in grid:
        print("".join(row))

def draw_maze2(grid, points):
    # copy the grid
    grid = [row.copy() for row in grid]

    # overwrite the vertices (except start and end)
    for p in points:
        val = get_grid(grid, p)
        if val != "S" and val != "E":
            set_grid(grid, p, "O")

    # print it out
    for row in grid:
        print("".join(row))
    

def get_full_data():
    with open(get_data_file("p16-data.txt")) as fp:
        data = fp.read()
    return data
        
def p16_part1():
    # run the tests
    m = Maze(Data1)
    path, cost = m.solve()
    # draw_maze(m.grid, path)
    assert cost == 7036
    
    m = Maze(Data2)
    path, cost = m.solve()
    # draw_maze(m.grid, path)
    assert cost == 11048
    
    # compute the solution
    m = Maze(get_full_data())
    path, cost = m.solve()
    # draw_maze(m.grid, path)
    return cost

def p16_part2():
    # run the tests
    m = Maze(Data1)
    points = m.solve2()
    # draw_maze2(m.grid, points)
    count = len(points)
    assert count == 45

    m = Maze(Data2)
    points = m.solve2()
    # draw_maze2(m.grid, points)
    count = len(points)
    assert count == 64

    # compute the solution
    sys.setrecursionlimit(20000)
    m = Maze(get_full_data())
    points = m.solve2()
    return len(points)

__all__ = ["p16_part1", "p16_part2"]
