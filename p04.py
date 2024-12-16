from .utils import *

def search1(data, x, y, dx, dy):
    word = "XMAS"
    word_l = len(word)
    
    m = len(data[0])
    n = len(data)

    def check_bounds(u, du, n):
        u_max = u + (word_l - 1)*du
        return u_max >= 0 and u_max < n

    # check bounds
    if not check_bounds(x, dx, m):
        return False
    if not check_bounds(y, dy, n):
        return False

    for s in range(word_l):
        u = x + s*dx
        v = y + s*dy
        if data[u][v] != word[s]:
            return False

    return True

def count_x1(data):
    # check the dimensions
    m = len(data[0])
    n = len(data)

    count = 0
    deltas = [(1, 0), (1, 1), (0, 1), (-1, 1),
              (-1, 0), (-1, -1), (0, -1), (1, -1)]
    for y in range(n):
        for x in range(m):
            for d in deltas:
                if search1(data, x, y, d[0], d[1]):
                    count += 1

    return count

Data1 = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

Data2 = """....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX"""

def get_data():
    with open(get_data_file("p04-data.txt")) as fp:
        data = fp.read().splitlines()
    return data

def p04_part1():
    # run the tests
    assert count_x1(Data1.splitlines()) == 18
    assert count_x1(Data2.splitlines()) == 18
    
    # compute the solution
    data = get_data()
    return count_x1(data)


def check_x(data, x, y):
    # the word is MAS and we check from "A" assuming bounds are 
    if data[x][y] != "A":
        return False

    # check for "M" and "S" at two vectors
    def check_ms(v0, v1):
        w = data[v0[0]][v0[1]] + data[v1[0]][v1[1]]
        return w == "MS" or w == "SM"

    # make the 4 points of the X
    xy = [(x + 1, y + 1),
          (x - 1, y + 1),
          (x - 1, y - 1),
          (x + 1, y - 1)]

    # check for the MAS cross (but "A" is already checked)
    if not check_ms(xy[0], xy[2]):
        return False
    if not check_ms(xy[1], xy[3]):
        return False

    return True

def count_x2(data):
    # check the dimensions
    m = len(data[0])
    n = len(data)

    count = 0
    for y in range(1,n-1):
        for x in range(1,m-1):
            if check_x(data, x, y):
                count += 1
    return count

Data3 = """.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
.........."""

def p04_part2():
    # run the tests
    assert count_x2(Data3.splitlines()) == 9

    # compute the solution
    data = get_data()
    return count_x2(data)

__all__ = ["p04_part1", "p04_part2"]
