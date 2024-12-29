from .utils import *

Data1 = """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02"""

Data2 = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""

Data3 = """x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00"""

GateFuncs = {
    "AND": lambda x, y: x & y,
    "XOR": lambda x, y: x ^ y,
    "OR": lambda x, y: x | y,
}
    
class Gates1:
    def __init__(self, data):
        self.values = {}  # maps wire name to value
        self.gates = {}   # maps output to (input0, input1, type)
        
        # parse the data
        lines = data.splitlines()
        
        # read the initial values
        for i in range(len(lines)):
            line = lines[i]
            if len(line) == 0:
                lines = lines[i+1:]
                break
            
            name, value = line.split(": ")
            self.values[name] = int(value)

        # read the gates
        for i in range(len(lines)):
            line = lines[i]
            items = line.split(" ")
            self.gates[items[4]] = (items[0], items[2], items[1])
            self.values[items[4]] = None

    def solve(self):
        # pull all the values of gates that start with "z"
        zs = [w for w in self.values if w.startswith("z")]
        zs = sorted(zs)
        zs = [self.evaluate(w) for w in zs]

        # evaluate the results
        result = 0
        for i, z in enumerate(zs):
            result += z * (1 << i)

        return result

    def evaluate(self, w):
        if self.values[w] is None:
            gate = self.gates[w]
            a = self.evaluate(gate[0])
            b = self.evaluate(gate[1])
            self.values[w] = GateFuncs[gate[2]](a, b)
        return self.values[w]

def get_full_data():
    with open(get_data_file("p24-data.txt")) as fp:
        data = fp.read()
    return data
    
def p24_part1():
    # run the tests
    for data in ((Data1, 4), (Data2, 2024)):
        gates = Gates1(data[0])
        n = gates.solve()
        assert n == data[1]

    # compute the solution
    gates = Gates1(get_full_data())
    return gates.solve()

def and_checks(n):
    # 0, 0
    x = [0]*n
    y = [0]*n
    z = [0]*n
    yield (x, y, z)

    # 1, 0
    x = [1]*n
    y = [0]*n
    z = [0]*n
    yield (x, y, z)

    # 0, 1
    x = [0]*n
    y = [1]*n
    z = [0]*n
    yield (x, y, z)

    # 1, 1
    x = [1]*n
    y = [1]*n
    z = [1]*n
    yield (x, y, z)

def add_checks(n):
    # 0 + 0 = 0
    x = [0]*n
    y = [0]*n
    z = [0]*n
    yield (x, y, z)

    # 1 + 0 = 1
    x = [1]*n
    y = [0]*n
    z = [1]*n
    yield (x, y, z)

    # all bits left, plus 1
    x = [1]*n
    y = [1] + [0]*(n-1)
    z = [0]*n
    yield (x, y, z)

    # 1 plus all bits right
    x = [1] + [0]*(n-1)
    y = [1]*n
    z = [0]*n
    yield (x, y, z)

    # alternating bits left and right
    x = ([0, 1]*n)[0:n]
    y = ([1, 0]*n)[0:n]
    z = [1]*n
    yield (x, y, z)

    # alternating the other way
    x = ([1, 0]*n)[0:n]
    y = ([0, 1]*n)[0:n]
    z = [1]*n
    yield (x, y, z)

    # all bits, both sides
    x = [1]*n
    y = [1]*n
    z = [0] + [1]*(n-1)
    yield (x, y, z)

    # last bits, 1 + 0
    x = [0]*(n-1) + [1]
    y = [0]*(n-1) + [0]
    z = [0]*(n-1) + [1]
    yield (x, y, z)

    # last bits, 1 + 0
    x = [0]*(n-1) + [0]
    y = [0]*(n-1) + [1]
    z = [0]*(n-1) + [1]
    yield (x, y, z)

    # last bits, 1 + 1
    x = [0]*(n-1) + [1]
    y = [0]*(n-1) + [1]
    z = [0]*n
    yield (x, y, z)

    # carry up to the last bit
    x = [1]*(n-1) + [0]
    y = [1] + [0]*(n-1)
    z = [0]*(n-1) + [1]
    yield (x, y, z)
    

def swap_n(a, n):
    # base case
    if n == 0:
        yield []
        return

    # determine all swaps containing the first element ...
    len_a = len(a)
    for i in range(1, len_a):
        part1 = a[1:i]
        part2 = a[i+1:]
        for c in swap_n(part1 + part2, n-1):
            yield [(a[0], a[i])] + c

    # ... and all swaps not containing the first element
    if len_a > 2*n:
        for c in swap_n(a[1:], n):
            yield c

def test_swap_n():
    data1 = [
        (["a","b","c"], 1,
         [[("a", "b")],
          [("a", "c")],
          [("b", "c")]]),
        (["a","b","c","d"], 1,
         [[("a", "b")],
          [("a", "c")],
          [("a", "d")],
          [("b", "c")],
          [("b", "d")],
          [("c", "d")]]),
        (["a","b","c","d"], 2,
         [[("a", "b"), ("c", "d")],
          [("a", "c"), ("b", "d")],
          [("a", "d"), ("b", "c")]]),
        (["a","b","c","d", "e"], 2,
         [[("a", "b"), ("c", "d")],
          [("a", "b"), ("c", "e")],
          [("a", "b"), ("d", "e")],
          
          [("a", "c"), ("b", "d")],
          [("a", "c"), ("b", "e")],
          [("a", "c"), ("d", "e")],
          
          [("a", "d"), ("b", "c")],
          [("a", "d"), ("b", "e")],
          [("a", "d"), ("c", "e")],
          
          [("a", "e"), ("b", "c")],
          [("a", "e"), ("b", "d")],
          [("a", "e"), ("c", "d")],
    
          [("b", "c"), ("d", "e")],
          [("b", "d"), ("c", "e")],
          [("b", "e"), ("c", "d")]]),
    ]
    for d in data1:
        r = [r for r in swap_n(d[0], d[1])]
        # print(f"r: {r}")
        assert r == d[2]
                
class Gates2:
    def __init__(self, data, checks):
        self.checks = checks # function to create checks
        self.values = {}     # maps wire name to value
        self.gates = {}      # maps output to (input0, input1, type)
        self.x = []          # list of X inputs
        self.y = []          # list of Y inputs
        self.z = []          # list of Z outputs
        
        # parse the data
        lines = data.splitlines()
        
        # determine the number of X's and Y's
        for i in range(len(lines)):
            line = lines[i]
            if len(line) == 0:
                lines = lines[i+1:]
                break
            
            name, value = line.split(": ")
            if name.startswith("x"):
                self.x.append(name)
            else:
                self.y.append(name)

        # read the gates
        for i in range(len(lines)):
            line = lines[i]
            items = line.split(" ")
            self.gates[items[4]] = (items[0], items[2], items[1])

        # create the names of the outputs
        self.z = [f"z{i:02}" for i in range(len(self.x))]

    def solve(self, num_swaps):
        # algorithm:
        #
        # - for an increasing subset of adjacent bits
        #   - find all gates (the corresponding outputs) that
        #     are non-zero for any test input
        #   - swap among these gates until the correct output is produced
        all_swaps = next(self.solve_n(1))
            
        # return the sorted string of names
        ret = []
        for s in all_swaps:
            ret += [s[0], s[1]]
        ret = sorted(ret)
        return ",".join(ret)

    def solve_n(self, n):
        # base case
        if n == len(self.x) + 1:
            yield []
            return
        
        if self.check(n):
            for swaps in self.solve_n(n+1):
                yield swaps
            return
            
        # find the gates that participate in this pair of bits
        gates = set()
        for data in self.checks(n):
            self.set_values(data[0], data[1])

            # get the positive gates
            g = self.get_nonzero_gates()
            gates.update(g)

        # add this output gate
        gates.add(self.z[n-1])

        # get the set of previous gates
        prev = set()
        if n > 1:
            for i in range(n-1):
                prev = prev.union(self.reachable(self.z[i]))

        # subtract the previous gates
        gates = gates - prev

        # run swaps until things work
        for swaps in self.check_swaps(n, gates, 1):
            for swaps2 in self.solve_n(n+1):
                yield swaps + swaps2

        for swaps in self.check_swaps(n, gates, 2):
            for swaps2 in self.solve_n(n+1):
                yield swaps + swaps2
                
    def check_swaps(self, j, gates, n):
        for swaps in swap_n(list(gates), n):
            # apply the swaps
            self.swap_gates(swaps)

            # check the result
            if self.check(j):
                yield swaps

            # reverse the swap
            self.swap_gates(swaps)

    def check(self, n):
        # run all the checks
        for data in self.checks(n):
            # set the values
            x, y, z0 = data
            self.set_values(x, y)

            # evaluate the bits
            z1 = [self.evaluate(self.z[i]) for i in range(len(x))]
            if not all([a == b for a, b in zip(z0, z1)]):
                return False
            
        return True

    def set_values(self, x, y):
        # set the values
        self.values = {}
        for k, v in zip(self.x, x):
            self.values[k] = v
        for k, v in zip(self.y, y):
            self.values[k] = v

    def get_nonzero_gates(self):
        gates = [w for w in self.gates if self.evaluate(w) == 1]
        return set(gates)

    def evaluate(self, w):
        if w not in self.values:
            # set a value to prevent cycles
            self.values[w] = -1

            # if a value wasn't set, there should be a gate
            if w not in self.gates:
                return -1
            
            gate = self.gates[w]
            a = self.evaluate(gate[0])
            b = self.evaluate(gate[1])
            self.values[w] = GateFuncs[gate[2]](a, b)
        return self.values[w]

    def reachable(self, w0):
        # compute the set of wires reachable from a wire
        wires = set()
        q = [w0]
        while len(q) > 0:
            # de-queue the next wire
            w = q.pop()

            # mark it visited
            wires.add(w)

            # check if it is the output of a gate
            if w in self.gates:
                g = self.gates[w]
                if g[0] not in wires:
                    q.append(g[0])
                if g[1] not in wires:
                    q.append(g[1])

        return wires

    def swap_gates(self, swaps):
        def swap_pair(p):
            w1, w2 = p
            g1 = self.gates[w1]
            g2 = self.gates[w2]
            self.gates[w1] = g2
            self.gates[w2] = g1

        for p in swaps:
            swap_pair(p)

def p24_part2():
    # run the tests
    test_swap_n()

    g = Gates2(Data3, and_checks)
    swaps = g.solve(2)
    assert swaps == "z00,z01,z02,z05"

    # compute the solution
    g = Gates2(get_full_data(), add_checks)
    s = g.solve(4)
    return s

__all__ = ["p24_part1", "p24_part2"]
