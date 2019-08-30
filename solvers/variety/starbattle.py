from claspy import *
from _base_ import Base
import itertools
import utils

class Starbattle(Base):
  def _solve(self):
    stars = utils.makeGrid(self.cols, self.rows, lambda: BoolVar())
    # starCount stars per row
    for y in range(self.rows):
      require(sum_bools(self.starCount, stars[y]))
    # starCount stars per column
    for x in range(self.cols):
      require(sum_bools(self.starCount, [stars[y][x] for y in range(self.rows)]))
    # stars can't be adjacent (including diagonal)
    for y in range(self.rows):
      for x in range(self.cols):
        threeByThree = [stars[y+dy][x+dx] if 0 <= y+dy < self.rows and 0 <= x+dx < self.cols else False for (dx,dy) in list(itertools.product([-1,0,1], [-1,0,1]))]
        require(cond(stars[y][x], sum_bools(1, threeByThree), True))
    # starCount stars per region. The technique used here is adopted from the fillimino example:
    # https://github.com/danyq/claspy/blob/master/examples/fillomino.py
    groups = utils.makeGrid(self.cols, self.rows, lambda: IntVar(0, self.cols*self.rows))
    roots = utils.makeGrid(self.cols, self.rows, lambda: BoolVar())
    groupAtoms = utils.makeGrid(self.cols, self.rows, lambda: Atom())
    for y in range(self.rows-1):
      for x in range(self.cols):
        if self.board.border[0][y][x]:
          require(groups[y][x] != groups[y+1][x])
        else:
          groupAtoms[y][x].prove_if(groupAtoms[y+1][x])
          groupAtoms[y+1][x].prove_if(groupAtoms[y][x])
          require(groups[y][x] == groups[y+1][x])
    for y in range(self.rows):
      for x in range(self.cols-1):
        if self.board.border[1][y][x]:
          require(groups[y][x] != groups[y][x+1])
        else:
          groupAtoms[y][x].prove_if(groupAtoms[y][x+1])
          groupAtoms[y][x+1].prove_if(groupAtoms[y][x])
          require(groups[y][x] == groups[y][x+1])
    for y in range(self.rows):
      for x in range(self.cols):
        groupAtoms[y][x].prove_if(stars[y][x])
        require(groupAtoms[y][x])
    num_solutions = solve(quiet=True)
    solution = [[utils.intify(x) for x in r] for r in stars]
    return (num_solutions, solution)

  def decode(self):
    self.decodeStarCount()
    self.decodeBorder()

  def decodeStarCount(self):
    barray = self.body.split("/")
    bd = self.board
    self.starCount = int(barray[0])
    self.body = barray[1] if len(barray) > 1 else ""
