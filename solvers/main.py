import json
import slither
import sudoku
import sys

inputObject = json.loads(sys.argv[1])
if inputObject['puzzleName'] == 'sudoku':
  sudoku.main(inputObject['encodedBoard'])
elif inputObject['puzzleName'] == 'slither':
  slither.main(inputObject['encodedBoard'])
else:
  print "Unsupported puzzle"