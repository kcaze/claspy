from claspy import *
from json import dumps
from _base_ import Base

class Sudoku(Base):
  def _solve(self):
    ans = [[IntVar(1,9) for j in range(9)] for i in range(9)]
    for i in range(9):
      require_all_diff(ans[i])
      require_all_diff([ans[j][i] for j in range(9)])
      require_all_diff([ans[j/3+i/3*3][j%3+i%3*3] for j in range(9)])
    for y in range(9):
      for x in range(9):
        if self.board.getCell(x,y) is not None:
          require(ans[y][x] == self.board.getCell(x,y))
    num_solutions = solve(quiet=True)
    if num_solutions == 0:
      return (Base.NO_SOLUTIONS, None)
    else:
      solution = [int(str(ans[i/9][i%9])) for i in range(81)]
      return (Base.UNIQUE_SOLUTION if num_solutions == 1 else Base.MULTIPLE_SOLUTIONS, solution)

  def decode(self):
    self.decodeNumber16()
