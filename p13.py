import re

from .utils import *

# Solve the integer linear system with a 2x2 matrix A and vector b.
# The matrix is a represented as a flat list:
#
#  [0 1]
#  [2 3]
#
def solve(A, b):
    det = A[0]*A[3] - A[1]*A[2]
    if det == 0:
        print("degenerate!")
        return None

    x = [1.0/det*(A[3]*b[0] - A[1]*b[1]),
         1.0/det*(-A[2]*b[0] + A[0]*b[1])]

    # convert to integer
    x = [round(x[0]), round(x[1])]

    # check the solution in integer
    b2 = [A[0]*x[0] + A[1]*x[1],
          A[2]*x[0] + A[3]*x[1]]

    if b2[0] != b[0] or b2[1] != b[1]:
        return None

    return x

Data1 = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

def parse_machines(data, part2=False):
    # a machine is represented by the tuple (a,b,p) where:
    #  a is the coordinate delta of the A button
    #  b is the coordinate delta of the B button
    #  p is the coordinate of the prize
    machines = []

    # make some re's to parse machines
    re_button = re.compile("Button .: X.([0-9]+), Y.([0-9]+)")
    re_prize = re.compile("Prize: X=([0-9]+), Y=([0-9]+)")

    def parse_coord(r, line):
        m = r.match(line)
        x = int(m.group(1))
        y = int(m.group(2))
        return (x,y)

    i = 0
    while i < len(data):
        a = parse_coord(re_button, data[i])
        b = parse_coord(re_button, data[i+1])
        p = parse_coord(re_prize, data[i+2])

        if part2:
            p = (p[0] + 10000000000000, p[1] + 10000000000000)
        
        machines.append((a, b, p))
        i += 4

    return machines

def solve_machine(m):
    # try solving the linear system
    a, b, p = m
    A = [a[0], b[0], a[1], b[1]]
    tokens = solve(A, p)

    # evaluate the cost
    cost = None
    if tokens is not None:
        cost = 3*tokens[0] + tokens[1]
    
    return cost

def solve_machines(data, part2=False):
    data = data.splitlines()
    machines = parse_machines(data, part2)
    
    total = 0
    for m in machines:
        cost = solve_machine(m)
        if cost is not None:
            total += cost
    return total

def get_full_data():
    with open(get_data_file("p13-data.txt")) as fp:
        data = fp.read()
    return data

def p13_part1():
    # run the tests
    A = [94, 22, 34, 67]
    b = [8400, 5400]
    x = solve(A, b)
    cost = 3*round(x[0]) + round(x[1])
    assert cost == 280

    cost = solve_machines(Data1)
    assert cost == 480

    # compute the solution
    return solve_machines(get_full_data())

Data2 = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=10000000008400, Y=10000000005400"""

Data3 = """Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=10000000012748, Y=10000000012176"""

Data4 = """Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=10000000007870, Y=10000000006450"""

Data5 = """Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=10000000018641, Y=10000000010279"""


def solve_single_machine(data):
    data = data.splitlines()
    m = parse_machines(data)[0]
    return solve_machine(m)

def p13_part2():
    # run the tests
    cost = solve_single_machine(Data2)
    assert cost is None
    
    cost = solve_single_machine(Data3)
    assert cost is not None

    cost = solve_single_machine(Data4)
    assert cost is None

    cost = solve_single_machine(Data5)
    assert cost is not None

    # compute the solution
    data = get_full_data()
    return solve_machines(data, True)

__all__ = ["p13_part1", "p13_part2"]
