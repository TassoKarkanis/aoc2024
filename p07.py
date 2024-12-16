from .utils import *

Equations = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

def get_data(data):
    eq = data.splitlines()

    # split into two parts
    eq = [e.split(": ") for e in eq]

    # split into all separate numbers
    eq = [[e[0]] + e[1].split(" ") for e in eq]

    # convert to int
    eq = [[int(x) for x in e] for e in eq]

    return eq

def get_test_data():
    return get_data(Equations)

def get_full_data():
    with open(get_data_file("p07-data.txt")) as fp:
        data = fp.read()
    return get_data(data)

def compute_part1(equations):
    # iterate over the equations
    count = 0
    calibration = 0
    for eq in equations:
        t = eq[0]    # desired total
        a = eq[1:]   # arguments of operators
        
        # compute the partial sums from the right
        sums = list(reversed(a))
        for i in range(1,len(sums)):
            sums[i] += sums[i-1]
        sums.reverse()

        # compute the partial products from the right
        prods = list(reversed(a))
        for i in range(1,len(prods)):
            prods[i] *= prods[i-1]
        prods.reverse()

        p = a.copy()           # partial evaluations
        ops = [0]*len(a)       # which operator was chosen (0 or 1)
        i = 0
        max_i = len(a) - 1
        match = False
        iters = 0
        while True:
            iters += 1
            # aggregate the next argument
            if ops[i] == 0:
                v = p[i] * a[i+1]
            else:
                v = p[i] + a[i+1]

            i += 1
            p[i] = v
            ops[i] = 0
                
            # check if we've found a solution
            if i == max_i and v == t:
                match = True
                break

            # increment
            if i == max_i or v > t:
                # go up and to the right
                while i >= 0:
                    i -= 1
                    if ops[i] == 0:
                        ops[i] = 1
                        break

                if i == -1:
                    break # all done

        # check if we matched
        if match:
            count += 1
            calibration += t

    return calibration

def p07_part1():
    # run the tests
    equations = get_test_data()
    assert compute_part1(equations) == 3749

    # compute the solution
    equations = get_full_data()
    return compute_part1(equations)
    
def compute_part2(equations):
    # iterate over the equations
    count = 0
    calibration = 0
    for eq in equations:
        t = eq[0]    # desired total
        a = eq[1:]   # arguments of operators
        
        # compute the partial sums from the right
        sums = list(reversed(a))
        for i in range(1,len(sums)):
            sums[i] += sums[i-1]
        sums.reverse()

        # compute the partial products from the right
        prods = list(reversed(a))
        for i in range(1,len(prods)):
            prods[i] *= prods[i-1]
        prods.reverse()

        p = a.copy()           # partial evaluations
        ops = [0]*len(a)       # which operator was chosen (0, 1, or 2)
        i = 0
        max_i = len(a) - 1
        match = False
        iters = 0
        while True:
            iters += 1
            # aggregate the next argument
            x = p[i]
            y = a[i+1]
            if ops[i] == 0:
                v = x * y
            elif ops[i] == 1:
                v = x + y
            else:
                v = int(str(x) + str(y))

            i += 1
            p[i] = v
            ops[i] = 0
                
            # check if we've found a solution
            if i == max_i and v == t:
                match = True
                break

            # increment
            if i == max_i or v > t:
                # go up and to the right
                while i >= 0:
                    i -= 1
                    if ops[i] < 2:
                        ops[i] += 1
                        break

                if i == -1:
                    break # all done

        # check if we matched
        if match:
            count += 1
            calibration += t

    return calibration

def p07_part2():
    # run the tests
    equations = get_test_data()
    assert compute_part2(equations) == 11387

    # compute the solution
    equations = get_full_data()
    return compute_part2(equations)
    
__all__ = ["p07_part1", "p07_part2"]
