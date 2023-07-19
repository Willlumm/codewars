# https://www.codewars.com/kata/5296bc77afba8baa690002d7/train/python

def get_row(puzzle, y):
    row = puzzle[y]
    return row

def get_col(puzzle, x):
    col = list(list(zip(*puzzle))[x])
    return col

def get_square(puzzle, x, y):
    x_min = (x // 3) * 3
    y_min = (y // 3) * 3
    square = [pos for row in puzzle[y_min : y_min+3] for pos in row[x_min : x_min+3]]
    return square

def is_complete(puzzle):
    for row in puzzle:
        if 0 in row:
            return False
    return True

def print_puzzle(puzzle):
    row_strs = []
    for row in puzzle:
        row_str = " ".join([str(pos) if pos != 0 else " " for pos in row])
        row_strs.append(row_str)
    puzzle_str = "\n".join(row_strs)
    print(puzzle_str)
    
def find_possibles(puzzle):
    possibles = [[set() for x in range(9)] for y in range(9)]
    for y, row in enumerate(possibles):
        for x, pos in enumerate(row):
            if puzzle[y][x] != 0:
                possibles[y][x] = {puzzle[y][x]}
                continue
            visible_nums = set(get_row(puzzle, y) + get_col(puzzle, x) + get_square(puzzle, x, y))
            possibles[y][x] = {n for n in range(1, 10)}.difference(visible_nums)
    return possibles

def sudoku(puzzle):
    """return the solved puzzle as a 2d array of 9 x 9"""
    while not is_complete(puzzle):
        possibles = find_possibles(puzzle)
        for y, row in enumerate(possibles):
            for x, pos in enumerate(row):
                if len(pos) == 1:
                    puzzle[y][x] = list(pos)[0]
    return puzzle

puzzle = [[5,3,0,0,7,0,0,0,0],
          [6,0,0,1,9,5,0,0,0],
          [0,9,8,0,0,0,0,6,0],
          [8,0,0,0,6,0,0,0,3],
          [4,0,0,8,0,3,0,0,1],
          [7,0,0,0,2,0,0,0,6],
          [0,6,0,0,0,0,2,8,0],
          [0,0,0,4,1,9,0,0,5],
          [0,0,0,0,8,0,0,7,9]]

print_puzzle(sudoku(puzzle))
