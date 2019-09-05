from _base_ import parseURL

import akari
import building
import hashi
import slither
import starbattle
import sudoku

solvers = {
  'akari': akari.Akari,
  'building': building.Building,
  'hashi': hashi.Hashi,
  'slither': slither.Slither,
  'starbattle': starbattle.Starbattle,
  'sudoku': sudoku.Sudoku,
}

def getPid(url):
  return parseURL(url)[0]
