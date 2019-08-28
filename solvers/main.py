import json
import os
import signal
import sys

import variety

TIMEOUT = 10
def handle_timeout(_signum, _frame):
  os.killpg(0, signal.SIGKILL)
os.setpgrp()
signal.signal(signal.SIGALRM, handle_timeout)
signal.alarm(TIMEOUT)

encodedURL = sys.argv[1]
pid = variety.getPid(encodedURL)
if pid in variety.solvers:
  solver = variety.solvers[pid](encodedURL)
  solver.solve()
else:
  print "Unsupported puzzle type %s" % pid