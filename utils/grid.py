
def on_grid(grid, p):
    M = len(grid[0])
    N = len(grid)

    x, y = p
    if x < 0 or x >= M:
        return False
    if y < 0 or y >= N:
        return False

    return True

def set_grid(grid, p, v):
    x, y = p
    grid[y][x] = v

def get_grid(grid, p):
    x, y = p
    return grid[y][x]

def copy_grid(g):
    g2 = [r.copy() for r in g]
    return g2

def print_grid(grid):
    for r in reversed(grid):
        print("".join(r))
