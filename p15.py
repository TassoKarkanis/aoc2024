from .utils import *

Data1 = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

Data2 = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

Data3 = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""

Data4 = """########
#......#
#.OOO@.#
#.OO...#
#..O...#
#......#
########

<vv<<v<^^<<^^"""

def draw_grid(grid):
    # print out the grid
    for line in grid:
        print("".join(map(str,line)))

    print()

# maps a move character to the delta position
MoveDelta = {
    "<": (-1, 0),
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
}
    
class Warehouse:
    def __init__(self, data):
        # split into lines
        lines = data.splitlines()

        # find the empty line
        e = 0
        for i, line in enumerate(lines):
            if line == "":
                e = i
                break

        # the first part is the grid
        self.grid = [[c for c in line] for line in lines[0:e]]
        self.m = len(self.grid[0])
        self.n = len(self.grid)

        # combine all the moves together
        self.moves = "".join(lines[e+1:])
        self.i = 0 # index of next move

        # determine the robot position
        for j in range(self.n):
            for i in range(self.m):
                p = (i, j)
                v = get_grid(self.grid, p)
                if v == "@":
                    self.robot = p
                    break

    def move(self):
        """movement for part1"""
        # return true if we're done moving
        if self.i >= len(self.moves):
            return True
        
        # changes to board if move is successful
        changes = [(self.robot, ".")]  # robot vacates spot

        # determine the direction of motion
        d = MoveDelta[self.moves[self.i]]

        # advance the move index
        self.i += 1

        # new position of robot
        p0 = v2_plus(self.robot, d)
        changes.append((p0, "@"))

        # see if we can complete the move
        p = p0
        moved = True
        while True:
            # look at the next spot
            val = get_grid(self.grid, p)

            # determine the next position over
            p2 = v2_plus(p, d)
            
            # if we hit a wall, we can't move
            if val == "#":
                moved = False
                break
            elif val == "O":
                # it's a box move, so speculatively move it over
                changes.append((p2,"O"))
            elif val == ".":
                # it's an empty space, so the move will succeed
                break

            # prepare for next iteration
            p = p2

        # complete the move, if possible
        if moved:
            # apply the changes to the board
            for c in changes:
                set_grid(self.grid, c[0], c[1])

            # update the robot position
            self.robot = p0

        # return True if we're done
        return self.i >= len(self.moves)

    def gps_sum(self):
        # read the box positions from the board
        total = 0
        for j in range(self.n):
            for i in range(self.m):
                p = (i, j)
                val = get_grid(self.grid, p)
                if val in "O[":
                    total += 100*j + i
        return total

    def widen(self):
        # replace every grid cell
        expansions = {
            "#": "##",
            "O": "[]",
            ".": "..",
            "@": "@."
        }
        grid = self.grid
        grid = [[expansions[c] for c in row] for row in grid]

        # make every grid cell separate again
        grid = ["".join(row) for row in grid]
        grid = [[c for c in row] for row in grid]
        self.grid = grid

        # update the grid dimensions
        self.m = 2*self.m

        # update the robot position
        x, y = self.robot
        self.robot = (2*x, y)

    def move2(self):
        """movement for part2"""
        # return true if we're done moving
        if self.i >= len(self.moves):
            return True
        
        # changes to board if move is successful
        changes = [(self.robot, ".")]  # robot vacates spot

        # determine the direction of motion
        motion = self.moves[self.i]
        d = MoveDelta[motion]

        # check if we are moving vertically
        vertical = motion in ("^", "v")

        # advance the move index
        self.i += 1

        # new position of robot
        p0 = v2_plus(self.robot, d)
        changes.append((p0, "@"))

        # we might now move multiple points with each "iteration"
        points = set()
        points.add(p0)

        # see if we can complete the move
        moved = True
        while len(points) > 0:
            new_points = set()
            for p in points:
                # look at the next spot
                val = get_grid(self.grid, p)
                
                # determine the next position over
                p2 = v2_plus(p, d)
                
                if val == "#":
                    # if we hit a wall, we can't move
                    moved = False
                    new_points = set()
                    break
                elif val == "[":
                    # it's a box move, so speculatively move it over
                    changes.append((p, "."))
                    changes.append((p2,"["))
                    new_points.add(p2)
                    if vertical:
                        # also add the right side of the box
                        pr = v2_plus(p, (1, 0))
                        pr2 = v2_plus(pr, d)
                        changes.append((pr, "."))
                        changes.append((pr2, "]"))
                        new_points.add(pr2)
                elif val == "]":
                    # it's a box move, so speculatively move it over
                    changes.append((p, "."))
                    changes.append((p2, "]"))
                    new_points.add(p2)
                    if vertical:
                        # also add the left side of the box
                        pl = v2_plus(p, (-1, 0))
                        pl2 = v2_plus(pl, d)
                        changes.append((pl, "."))
                        changes.append((pl2, "["))
                        new_points.add(pl2)
                elif val == ".":
                    pass # it's an empty space, so the move will succeed
                
            # prepare for next iteration
            points = new_points

        # complete the move, if possible
        if moved:
            # apply the changes to the board in reverse order
            for c in reversed(changes):
                set_grid(self.grid, c[0], c[1])

            # update the robot position
            self.robot = p0

        # return True if we're done
        return self.i >= len(self.moves)

def get_full_data():
    with open(get_data_file("p15-data.txt")) as fp:
        data = fp.read()
    return data
    
def p15_part1():
    # run the tests
    w = Warehouse(Data1)
    assert w.robot == (2, 2)
    while not w.move():
        pass
    assert w.robot == (4, 4)
    assert w.gps_sum() == 2028

    w = Warehouse(Data2)
    assert w.robot == (4, 4)
    # draw_grid(w.grid)
    while True:
        done = w.move()
        if done:
            break
    assert w.robot == (3, 4)
    assert w.gps_sum() == 10092

    # compute the solution
    data = get_full_data()
    w = Warehouse(data)
    while not w.move():
        pass
    return w.gps_sum()

def run2(w, quiet=True):
    # widen the grid
    w.widen()

    # show the initial grid
    if not quiet:
        print("initial")
        draw_grid(w.grid)

    # simulate all moves
    while True:
        if not quiet:
            print(f"move: {w.moves[w.i]}")
            
        done = w.move2()

        if not quiet:
            draw_grid(w.grid)
            
        if done:
            break


def p15_part2():
    # run the tests
    w = Warehouse(Data2)
    w.widen()
    # draw_grid(w.grid)

    w = Warehouse(Data3)
    run2(w)

    w = Warehouse(Data4)
    run2(w)

    w = Warehouse(Data2)
    run2(w)
    assert w.gps_sum() == 9021

    # compute the solution
    data = get_full_data()
    w = Warehouse(data)
    run2(w)
    return w.gps_sum()

__all__ = ["p15_part1", "p15_part2"]
