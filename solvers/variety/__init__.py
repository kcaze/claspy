from _base_ import parseURL

import slither
import starbattle
import sudoku

solvers = {
  'slither': slither.Slither,
  'starbattle': starbattle.Starbattle,
  'sudoku': sudoku.Sudoku,
}

def getPid(url):
  return parseURL(url)[0]
