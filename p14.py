import re

from .utils import *

Data1 = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

def parse_robots(data):
    # robots are represented as the tuple (p, v)
    robots = []

    # make an re
    r = re.compile("p=(-*[0-9]+),(-*[0-9]+) v=(-*[0-9]+),(-*[0-9]+)")

    for line in data:
        m = r.match(line)
        px = int(m.group(1))
        py = int(m.group(2))
        vx = int(m.group(3))
        vy = int(m.group(4))

        p = (px, py)
        v = (vx, vy)
        robots.append((p, v))

    return robots

def draw_grid(grid):
    # print out the grid
    for line in grid:
        print("".join(map(str,line)))

    print()

class Simulation:
    def __init__(self, robots, m, n):
        self.robots = robots  # robots in the simulation
        self.m = m            # width of room
        self.n = n            # height of room

    def step(self):
        # update the positions of the robots
        robots2 = []
        for r in self.robots:
            # get position and velocity
            p, v = r

            # move
            p = v2_plus(p, v)

            # respect the limits of the room
            def teleport(u, u_max):
                if u < 0:
                    u += u_max
                if u >= u_max:
                    u -= u_max
                return u
            x, y = p
            p = (teleport(x,self.m), teleport(y,self.n))

            # store it
            r = (p, v)
            robots2.append(r)

        self.robots = robots2

    def safety_factor(self):
        # mid points of range
        mx = self.m // 2
        my = self.n // 2

        # count the robots per quadrant
        q = [0, 0, 0, 0]
        for r in self.robots:
            x, y = r[0]
            if x < mx and y < my:
                q[0] += 1
            elif x > mx and y < my:
                q[1] += 1
            elif x < mx and y > my:
                q[2] += 1
            elif x > mx and y > my:
                q[3] += 1

        return q[0]*q[1]*q[2]*q[3]

    def tree_factor(self):
        # get the robot positions
        pos = {}
        for r in self.robots:
            p = r[0]
            pos[p] = True

        # for robot, count the number of adjacent occupied cells
        count = 0
        adj = (-1, 0, 1)
        for p in pos:
            x, y = p
            for i in adj:
                for j in adj:
                    # skip the robot itself
                    if i == 0 and j == 0:
                        continue

                    # check if this adjacent cell has a robot
                    p2 = (x+i, y+j)
                    if p2 in pos:
                        count += 1
        return count

    def get_grid(self):
        # make a grid of zeros
        grid = [[0]*self.m for i in range(self.n)]

        # increment at robot positions
        for r in self.robots:
            x, y = r[0]
            grid[y][x] += 1

        # clear zeros to "."
        grid = [["." if x == 0 else x for x in row] for row in grid]
        return grid

    def draw(self):
        grid = self.get_grid()
        draw_grid(grid)

def get_full_data():
    with open(get_data_file("p14-data.txt")) as fp:
        data = fp.read()
    return data
        
def p14_part1():
    # run the tests
    robots = parse_robots(Data1.splitlines())
    s = Simulation(robots, 11, 7)
    # s.draw()

    robots = parse_robots(["p=2,4 v=2,-3"])
    s = Simulation(robots, 11, 7)
    for i in range(5):
        # print(f"after {i} seconds")
        # s.draw()
        s.step()

    robots = parse_robots(Data1.splitlines())
    s = Simulation(robots, 11, 7)
    for i in range(100):
        s.step()
    f = s.safety_factor()
    assert f == 12

    # compute the solution
    data = get_full_data()
    robots = parse_robots(data.splitlines())
    s = Simulation(robots, 101, 103)
    for i in range(100):
        s.step()
    f = s.safety_factor()
    return f
    
def p14_part2():
    # compute the solution
    data = get_full_data()
    robots = parse_robots(data.splitlines())
    s = Simulation(robots, 101, 103)
    max_i = None
    max_f = -1
    max_grid = None
    for i in range(10000):
        f = s.tree_factor()
        if f > max_f:
            max_i = i
            max_f = f
            max_grid = s.get_grid()

        s.step()
        
    # print(f"max_i({max_i}) max_f({max_f})")
    # draw_grid(max_grid)
    return max_i
    

__all__ = ["p14_part1", "p14_part2"]
