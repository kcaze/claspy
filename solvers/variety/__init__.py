from _base_ import parseURL
import sudoku

solvers = {
  'sudoku': sudoku.Sudoku,
}

def getPid(url):
  return parseURL(url)[0]