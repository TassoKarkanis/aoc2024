from .utils import *

Data1 = """029A: <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
980A: <v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A
179A: <v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
456A: <v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A
379A: <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"""

FullData = """964A
140A
413A
670A
593A"""

# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+
DoorButtons = {
    "X": (0, 0),  # gap
    "0": (1, 0),
    "A": (2, 0),
    "1": (0, 1),
    "2": (1, 1),
    "3": (2, 1),
    "4": (0, 2),
    "5": (1, 2),
    "6": (2, 2),
    "7": (0, 3),
    "8": (1, 3),
    "9": (2, 3),
}

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > | 
# +---+---+---+
RemoteButtons = {
    "<": (0, 0),
    "v": (1, 0),
    ">": (2, 0),
    "X": (0, 1),  # gap
    "^": (1, 1),
    "A": (2, 1),
}

Movements = {
    ">": (1, 0),
    "^": (0, 1),
    "<": (-1, 0),
    "v": (0, -1),
}

def combinations2(a, m, b, n):
    if m == n and n == 0:
        return
    elif m == 0:
        yield [b] * n
    elif n == 0:
        yield [a] * m
    else:
        for s in combinations2(a, m-1, b, n):
            yield [a] + s
        for s in combinations2(a, m, b, n-1):
            yield [b] + s

def test_combinations2():
    data = (
        (("a", 0, "b", 0), []),
        (("a", 1, "b", 0), ["a"]),
        (("a", 0, "b", 1), ["b"]),
        (("a", 2, "b", 0), ["aa"]),
        (("a", 0, "b", 2), ["bb"]),
        (("a", 1, "b", 1), ["ab", "ba"]),
        (("a", 2, "b", 1), ["aab", "aba", "baa"]),
        (("a", 2, "b", 2), ["aabb", "abab", "abba",
                            "baab", "baba", "bbaa"]),
    )
    for d in data:
        q = d[0]
        out = [s for s in combinations2(q[0], q[1], q[2], q[3])]
        out = ["".join(o) for o in out]
        assert out == d[1]

class GeneratorBase:
    def __init__(self, buttons):
        self.buttons = buttons    # map of button name to position
        self.gap = buttons["X"]   # location of gap
        self.cur = buttons["A"]   # current position
        
    def generate_paths(self, p):
        if p == self.cur:
            return ["A"]

        # compute the change to get there
        d = v2_minus(p, self.cur)

        # all possible ways to get there
        dx, dy = d
        m = abs(dx)
        dx = ">" if dx > 0 else "<"
        n = abs(dy)
        dy = "^" if dy > 0 else "v"
        paths = combinations2(dx, m, dy, n)
        paths = ["".join(p) for p in paths]

        # filter out paths that contain the gap
        paths = [p for p in paths if self.gap not in self.generate_positions(p)]

        return paths

    def generate_positions(self, path):
        # generate a list of positions from a path
        p1 = self.cur
        positions = []
        for m in path:
            d = Movements[m]
            p2 = v2_plus(p1, d)
            positions.append(p2)
            p1 = p2
        return positions

class Generator1(GeneratorBase):
    def __init__(self, buttons, sub_gen=None):
        super().__init__(buttons)
        
        self.sub_gen = None       # sub-generator's generate() function
        self.memos = {}           # map of (p1,p2) -> shortest path

        if sub_gen is None:
            # the default sub-generator is the identity
            self.sub_gen = lambda x: x
        else:
            self.sub_gen = sub_gen.generate
        
    def generate(self, seq):
        # compute each step
        output = ""
        for s in seq:
            # determine the new position
            p = self.buttons[s]

            # determine the shortest path to get there
            min_path = self.shortest_path(p)

            # accumulate the path
            output += min_path

            # store the new position
            self.cur = p

        return output

    def shortest_path(self, p):
        if p == self.cur:
            return "A"

        # check if we have memoized the shortest path
        key = (self.cur, p)
        if key in self.memos:
            return self.memos[key]

        paths = self.generate_paths(p)

        # invoke the sub-generator for all these paths
        min_path_len = sys.maxsize
        min_path = None
        for path in paths:
            sub_path = self.sub_gen(path + "A")
            sub_path_len = len(sub_path)
            if sub_path_len < min_path_len:
                min_path_len = sub_path_len
                min_path = sub_path

        # store this path
        self.memos[key] = min_path
        
        return min_path

class Generator2(GeneratorBase):
    def __init__(self, buttons, sub_gen=None):
        super().__init__(buttons)
        
        self.sub_gen = None       # sub-generator's generate() function
        self.memos = {}           # map of (p1,p2) -> length of shortest path

        if sub_gen is None:
            # the default sub-generator is the identity
            self.sub_gen = lambda x: len(x)
        else:
            self.sub_gen = sub_gen.generate
        
    def generate(self, seq):
        # compute each step
        total_len = 0
        for s in seq:
            # determine the new position
            p = self.buttons[s]

            # determine the shortest path to get there
            path_len = self.shortest_path(p)

            # accumulate the path
            total_len += path_len

            # store the new position
            self.cur = p

        return total_len

    def shortest_path(self, p):
        if p == self.cur:
            return 1 #  path is just "A"

        # check if we have memoized the shortest path
        key = (self.cur, p)
        if key in self.memos:
            return self.memos[key]

        paths = self.generate_paths(p)

        # invoke the sub-generator for all these paths
        min_path_len = sys.maxsize
        for path in paths:
            sub_path_len = self.sub_gen(path + "A")
            if sub_path_len < min_path_len:
                min_path_len = sub_path_len

        # store this path
        self.memos[key] = min_path_len
        
        return min_path_len

def evaluate(buttons, seq):
    # reverse the buttons map
    rev_buttons = {}
    for name, pos in buttons.items():
        rev_buttons[pos] = name

    p = buttons["A"]
    result = ""
    for s in seq:
        if s == "A":
            result += rev_buttons[p]
        else:
            v = Movements[s]
            p = v2_plus(p, v)

    return result
    
def checksum(s):
    # compute a simple order-independent checksum for a string
    s = "".join(sorted(s))
    return hash(s)
    
def p21_part1():
    # run the tests
    test_combinations2()
    
    g = Generator1(DoorButtons)
    s = g.generate("029A")
    # print(s)
    assert checksum(s) == checksum("<A^A>^^AvvvA")
    assert evaluate(DoorButtons, s) == "029A"

    # combine two robots
    g2 = Generator1(RemoteButtons)
    g1 = Generator1(DoorButtons, g2)
    s = g1.generate("029A")
    # print(s)
    assert checksum(s) == checksum("v<<A>>^A<A>AvA<^AA>A<vAAA>^A")
    assert evaluate(DoorButtons,evaluate(RemoteButtons,s)) == "029A"
    
    # combine three robots
    g3 = Generator1(RemoteButtons)
    g2 = Generator1(RemoteButtons, g3)
    g1 = Generator1(DoorButtons, g2)

    # define the evaluation function
    def e(s):
        s = evaluate(RemoteButtons, s)
        s = evaluate(RemoteButtons, s)
        s = evaluate(DoorButtons, s)
        return s
    
    data = Data1.splitlines()
    for line in data:
        seq = line[0:4]
        # print(f"seq: {seq}")
        buttons = line[6:]
        s = g1.generate(seq)
        # print(f"  actual:   {checksum(s)} {s}")
        # print(f"  expected: {checksum(buttons)} {buttons}")
        # print(f"  e: {e(s)}")

    # compute the solutions
    g3 = Generator1(RemoteButtons)
    g2 = Generator1(RemoteButtons, g3)
    g1 = Generator1(DoorButtons, g2)
    data = FullData.splitlines()
    total = 0
    for code in data:
        numeric_code = code.replace("A", "")
        s = g1.generate(code)
        total += int(numeric_code) * len(s)
    return total

def p21_part2():
    g = None
    for i in range(25):
        g2 = Generator2(RemoteButtons, g)
        g = g2
    g = Generator2(DoorButtons, g)
    data = FullData.splitlines()
    total = 0
    for code in data:
        numeric_code = code.replace("A", "")
        path_len = g.generate(code)
        total += int(numeric_code) * path_len
    return total

__all__ = ["p21_part1", "p21_part2"]
