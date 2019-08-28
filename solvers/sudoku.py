from claspy import *
from parser import parse

def main(encodedBoard):
  puzzle = parse(encodedBoard)
  sudoku = [[IntVar(1,9) for j in range(9)] for i in range(9)]
  for i in range(9):
    require_all_diff(sudoku[i])
    require_all_diff([sudoku[j][i] for j in range(9)])
    require_all_diff([sudoku[j/3+i/3*3][j%3+i%3*3] for j in range(9)])
  for y in range(9):
    for x in range(9):
      if self.board.getCell(x,y) is not None:
        require(sudoku[y][x] == self.board.getCell(x,y))
  solve(quiet=True)
  for y in range(9):
    for x in range(9):
      print sudoku[y][x],
    print