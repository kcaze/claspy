from _base_ import parseURL

import akari
import slither
import starbattle
import sudoku

solvers = {
  'akari': akari.Akari,
  'slither': slither.Slither,
  'starbattle': starbattle.Starbattle,
  'sudoku': sudoku.Sudoku,
}

def getPid(url):
  return parseURL(url)[0]
