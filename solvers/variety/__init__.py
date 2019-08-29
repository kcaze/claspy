from _base_ import parseURL

import slither
import sudoku

solvers = {
  'slither': slither.Slither,
  'sudoku': sudoku.Sudoku,
}

def getPid(url):
  return parseURL(url)[0]
