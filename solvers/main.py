import json
import os
import signal
import sys

import slither
import starbattle
import sudoku

TIMEOUT = 10
def handle_timeout(_signum, _frame):
  os.killpg(0, signal.SIGKILL)
os.setpgrp()
signal.signal(signal.SIGALRM, handle_timeout)
signal.alarm(TIMEOUT)

inputObject = json.loads(sys.argv[1])
if inputObject['puzzleName'] == 'sudoku':
  sudoku.main(inputObject['encodedBoard'])
elif inputObject['puzzleName'] == 'slither':
  slither.main(inputObject['encodedBoard'])
elif inputObject['puzzleName'] == 'starbattle':
  starbattle.main(inputObject['encodedBoard'])
else:
  print "Unsupported puzzle"