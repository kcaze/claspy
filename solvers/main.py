import json
import sudoku
import sys

inputObject = json.loads(sys.argv[1])
if inputObject['puzzleName'] == 'sudoku':
  sudoku.main(inputObject['encodedBoard'])
else:
  print "Unsupported puzzle"