from claspy import *
from parser import parse

def main(encodedBoard):
  puzzle = parse(encodedBoard)
  sudoku = [[IntVar(1,9) for j in range(9)] for i in range(9)]
  for i in range(9):
    require_all_diff(sudoku[i])
    require_all_diff([sudoku[j][i] for j in range(9)])
    require_all_diff([sudoku[j/3+i/3*3][j%3+i%3*3] for j in range(9)])
  for i in range(9):
    for j in range(9):
      if puzzle[i][j] is not None:
        require(sudoku[i][j] == int(puzzle[i][j]))
  solve(quiet=True)
  for i in range(9):
    for j in range(9):
      print sudoku[i][j],
    print