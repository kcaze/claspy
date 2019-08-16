from claspy import *

def main(encodedBoard):
  puzzle = [row.split("_")[:-1] for row in encodedBoard.split("/")[:-1]]
  sudoku = [[IntVar(1,9) for j in range(9)] for i in range(9)]
  for i in range(9):
    require_all_diff(sudoku[i])
    require_all_diff([sudoku[j][i] for j in range(9)])
    require_all_diff([sudoku[j/3+i/3*3][j%3+i%3*3] for j in range(9)])
  for i in range(9):
    for j in range(9):
      if puzzle[i][j] != '.':
        require(sudoku[i][j] == int(puzzle[i][j]))
  solve(quiet=True)
  for i in range(9):
    for j in range(9):
      print sudoku[i][j],
    print