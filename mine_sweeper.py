#  https://www.codewars.com/kata/57ff9d3b8f7dda23130015fa/train/python

# from preloaded import open

def parse_map(map):
    grid = []
    row = []
    for char in map:
        if char in {"?", "0"}:
            row.append(char)
        elif char == "\n":
            map.append(row)
            row = []
    return grid

def get_adjs(grid, x, y):
    adjs = []
    for xi in range(x-1, x+2):
        for yi in range(y-1, y+2):
            if 0 <= xi < len(grid[0]) and 0 <= yi < len(grid) and not (xi == x and yi == y):
                adjs.append(xi, yi)
    return adjs

def solve_mine(map, n):
    grid = parse_map(map)
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "0":
                for xi, yi in get_adjs(grid, x, y):
                    grid[yi][xi] = open(yi, xi)
            elif cell not in {"?", "X"}:
                adjs = get_adjs(grid, x, y)
                if len(adjs) == int(cell):
                    for xi, yi in adjs:
                        grid[yi][xi] = "X"
                
                
            
    # coding and coding...
    # open(0,1)
    return '?'


gamemap = """
? ? ? ? ? ?
? ? ? ? ? ?
? ? ? 0 ? ?
? ? ? ? ? ?
? ? ? ? ? ?
0 0 0 ? ? ?
""".strip()

print(gamemap)