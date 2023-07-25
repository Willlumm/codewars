# https://www.codewars.com/kata/52bb6539a4cf1b12d90005b7/train/python

def assign_ship(ships, xy):
    x, y = xy
    if len(set(ships).intersection({(x+1, y+1), (x-1, y+1), (x-1, y-1), (x+1, y-1)})) > 0:
        return False
    adj = set(ships).intersection({(x+1, y), (x, y+1), (x-1, y), (x, y-1)})
    if not ships:
        ships[(x, y)] = 1
    elif len(adj) == 0:
        ships[(x, y)] = max(ships.values()) + 1
    elif len(adj) == 1:
        ships[(x, y)] = ships[adj.pop()]
    else:
        return False
    return True

def validate_battlefield(field):
    ships = {}
    for y, row in enumerate(field):
        for x, cell in enumerate(row):
            if cell and not assign_ship(ships, (x, y)):
                return False
    len_counts = [0] * 5
    for id in set(ships.values()):
        ship_len = list(ships.values()).count(id)
        if ship_len > 4:
            return False
        len_counts[ship_len] += 1
    if len_counts != [0, 4, 3, 2, 1]:
        return False
    return True

field = [
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

print(validate_battlefield(field))