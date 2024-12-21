from .utils import *

Data1 = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

def decompose(s1, s2):
    # Returns a list of tuples (s1, s2, s3).  Joining each tuple
    # results in s1 and s2 brackets the "center" character of s.
    # 
    # Make the "center" substring string that includes all possible
    # positions of s2.
    s1_len = len(s1)
    s2_len = len(s2)
    mid = s1_len // 2
    c0 = max(0, mid - (s2_len - 1))
    c1 = min(s1_len, mid + s2_len)
    center = s1[c0:c1]

    offset = 0
    results = []
    while True:
        pos = center.find(s2, offset)
        if pos == -1:
            break

        i = c0 + pos
        j = i + s2_len
        left = s1[0:i]
        right = s1[j:]
        results.append((left, s2, right))

        offset = pos + 1
    return results

def test_decompose():
    data = [
        ("", "r", []),
        ("r", "r", [("", "r", "")]),
        ("rr", "r", [("r", "r", "")]),
        ("rar", "a", [("r", "a", "r")]),
        ("rrr", "rr", [("", "rr", "r"),
                       ("r", "rr", "")]),
        ("rrrr", "rr", [("r", "rr", "r"),
                        ("rr", "rr", "")]),
        ("rrrrr", "rr", [("r", "rr", "rr"),
                         ("rr", "rr", "r")]),
        ("rrrrrr", "rrr", [("r", "rrr", "rr"),
                           ("rr", "rrr", "r"),
                           ("rrr", "rrr", "")]),
        ("arararar", "ar", [("arar", "ar", "ar")]),
        ("arararar", "ra", [("ara", "ra", "rar")]),
    ]
    for d in data:
        result = decompose(d[0], d[1])
        assert result == d[2]

class Solver:
    def __init__(self, data):
        self.atoms = set()
        self.patterns = []
        
        lines = data.splitlines()

        # read the atoms
        self.atoms = set(lines[0].replace(" ","").split(","))

        # read the patterns
        self.patterns = lines[2:]

    def solve(self):
        # make memos a copy of the atoms
        self.memos = set(list(self.atoms))
        
        count = 0
        for pattern in self.patterns:
            ok = self.solve_pattern(pattern)
            if ok:
                count += 1

        return count

    def solve_pattern(self, pattern):
        if len(pattern) == 0:
            return True
        if pattern in self.memos:
            return True
        
        for atom in self.atoms:
            parts = decompose(pattern, atom)
            for p in parts:
                if self.solve_pattern(p[0]) and self.solve_pattern(p[2]):
                    self.memos.add(pattern)
                    return True
        return False

    def solve2(self):
        # make memos a map of pattern to count
        self.memos = {}

        # solve the atoms
        atoms = sorted(self.atoms, key=lambda a: len(a))
        self.atoms = set()
        for atom in atoms:
            count = self.solve2_pattern(atom) + 1
            self.memos[atom] = count
            self.atoms.add(atom)

        # solve all the patterns
        count = 0
        for pattern in self.patterns:
            c = self.solve2_pattern(pattern)
            count += c

        return count

    def solve2_pattern(self, pattern):
        if len(pattern) == 0:
            return 1
        if pattern in self.memos:
            return self.memos[pattern]

        count = 0
        for atom in self.atoms:
            parts = decompose(pattern, atom)
            for p in parts:
                c0 = self.solve2_pattern(p[0])
                if c0 == 0:
                    continue

                c1 = self.solve2_pattern(p[2])
                count += c0 * c1

        # memoize the pattern
        self.memos[pattern] = count
        return count

def get_full_data():
    with open(get_data_file("p19-data.txt")) as fp:
        data = fp.read()
    return data
    
def p19_part1():
    # run the tests
    test_decompose()
    
    s = Solver(Data1)
    count = s.solve()

    # compute the solution
    s = Solver(get_full_data())
    count = s.solve()
    return count

def p19_part2():
    # run the tests
    s = Solver(Data1)
    count = s.solve2()
    assert count == 16

    # compute the solution
    s = Solver(get_full_data())
    count = s.solve2()
    return count

    
__all__ = ["p19_part1", "p19_part2"]
