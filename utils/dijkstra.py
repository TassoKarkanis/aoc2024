import sys

# The graph is represented as:
#
#   G = (V, E, EC)
#
# where:
#
#   V: an iterable of the vertices of the graph
#
#   E: edges as a map of vertex to set of vertices
#
#   EC: cost of edges as map of (v1,v2) -> cost

# function Dijkstra(Graph, source):
# for each vertex v in Graph.Vertices:
#     dist[v] ← INFINITY
#     prev[v] ← UNDEFINED
#     add v to Q
# dist[source] ← 0
# 
# while Q is not empty:
#     u ← vertex in Q with minimum dist[u]
#     remove u from Q
#    
#     for each neighbor v of u still in Q:
#         alt ← dist[u] + Graph.Edges(u, v)
#         if alt < dist[v]:
#             dist[v] ← alt
#             prev[v] ← u
# 
# return dist[], prev[]

def dijkstra(Graph, source):
    # Don't use sys.maxsize because we'll be adding to it
    Infinity = sys.maxsize // 4
    
    # initialize the distances
    dist = {}
    for v in Graph[0]:
        dist[v] = Infinity
        
    dist[source] = 0

    # We'll keep Q small by storing only the unvisited vertices in it.
    # So we also keep a set of the visited vertices.
    Q = set()
    Q.add(source)
    visited = set()
    
    # Generate dist and prev.  We implement the form of Dijkstra's
    # algorithm where all shortest paths can be computed, so the value
    # of prev is a set of predecessors.
    prev = {}
    
    while len(Q) > 0:
        # determine the unvisited vertex with minimum distance
        u = min(Q, key=lambda x: dist[x])
        Q.remove(u)

        # mark this one visited
        visited.add(u)

        # u may not have neighbours
        if u not in Graph[1]:
            continue
        
        for v in Graph[1][u]:
            # ignore if it has already been processed
            if v in visited:
                continue

            # add it for consideration later if necessary
            Q.add(v)

            e = (u, v)
            alt = dist[u] + Graph[2][e]
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = set()
                prev[v].add(u)
            elif alt == dist[v]:
                prev[v].add(u)

    return dist, prev

# function shortest_path():
# S ← empty sequence
# u ← target
# if prev[u] is defined or u = source:          // Proceed if the vertex is reachable
#     while u is defined:                       // Construct the shortest path with a stack S
#         insert u at the beginning of S        // Push the vertex onto the stack
#         u ← prev[u]                           // Traverse from target to source

def shortest_path(source, target, dist, prev):
    S = []
    u = target
    if u in prev or u == source:
        while True:
            S.append(u)
            if u not in prev:
                break

            # get some predecessor of u
            for u in prev[u]:
                break
    S.reverse()
    return S
