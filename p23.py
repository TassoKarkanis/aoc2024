from .utils import *

Data1 = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""

def get_data(data):
    # split the lines
    lines = data.splitlines()
    conn = [tuple(line.split("-")) for line in lines]
    return conn

def get_full_data():
    with open(get_data_file("p23-data.txt")) as fp:
        data = fp.read()
    return get_data(data)

def solve(conn):
    # maps a computer name to list of names that are lexicographically greater
    sets = {}

    # set of all pairs (p1,p2) that are connected
    connected = set()
    
    for pair in conn:
        # reorder pair, if necessary
        p1, p2 = pair
        if p1 > p2:
            p1, p2 = p2, p1

        # update sets for this pair
        if p1 not in sets:
            sets[p1] = [p2]
        else:
            sets[p1].append(p2)

        # update connected
        connected.add((p1, p2))
        connected.add((p2, p1))

    def connected_pairs(names):
        count = 0
        # any two choices in names will work
        for i, p2 in enumerate(names):
            for j in range(i+1, len(names)):
                p3 = names[j]
                if (p2, p3) in connected:
                    count += 1
        return count
        
    # count the 3-sets that have an element that starts with "t"
    count = 0
    for p1, names in sets.items():
        # ignore degenerate sets
        n = len(names)
        if n < 2:
            continue

        # special case when p1 starts with "t"
        if p1.startswith("t"):
            count += connected_pairs(names)
            continue

        # get the subsets of names that start with "t" and that don't
        names1 = [p for p in names if p.startswith("t")]
        names2 = [p for p in names if not p.startswith("t")]

        # any two choices from the first group will work
        count += connected_pairs(names1)

        # any pair from the first and second group works
        for p2 in names1:
            for p3 in names2:
                if (p2, p3) in connected:
                    count += 1

    return count

def p23_part1():
    conn = get_data(Data1)
    count = solve(conn)
    assert count == 7

    # compute the solution
    conn = get_full_data()
    count = solve(conn)
    return count

# algorithm BronKerbosch2(R, P, X) is
#     if P and X are both empty then
#         report R as a maximal clique
#     choose a pivot vertex u in P ⋃ X
#     for each vertex v in P \ N(u) do
#         BronKerbosch2(R ⋃ {v}, P ⋂ N(v), X ⋂ N(v))
#         P := P \ {v}
#         X := X ⋃ {v}

# Implement BronKerbosch2 where G is a map of vertex to set of neighbours.
def BronKerbosch2(G, R, P, X):
    # first condition
    if len(P) == 0 and len(X) == 0:
        yield R
        return

    # choose a pivot vertex
    if len(P) != 0:
        for u in P:
            break
    else:
        for u in X:
            break

    for v in (P - G[u]):
        for c in BronKerbosch2(G, R | set([v]), P & G[v], X & G[v]):
            yield c
        P.remove(v)
        X.add(v)

def solve2(conn):
    G = {}

    def add_edge(v1, v2):
        if v1 not in G:
            s = set()
            s.add(v2)
            G[v1] = s
        else:
            G[v1].add(v2)
    
    for pair in conn:
        p1, p2 = pair
        add_edge(p1, p2)
        add_edge(p2, p1)

    V = set([v for v in G])
    max_clique = set()
    for c in BronKerbosch2(G, set(), V, set()):
        if len(c) > len(max_clique):
            max_clique = c

    password = ",".join(sorted(max_clique))
    return password
        
def p23_part2():
    # run the tests
    conn = get_data(Data1)
    password = solve2(conn)
    assert password == "co,de,ka,ta"

    # compute the solution
    conn = get_full_data()
    password = solve2(conn)
    return password

__all__ = ["p23_part1", "p23_part2"]
