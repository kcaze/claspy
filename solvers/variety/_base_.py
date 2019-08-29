import math
import re

class Board:
  def __init__(self, cols, rows):
    self.cell = initCell(cols, rows)
    self.border = initBorder(cols, rows)
    self.cols = cols
    self.rows = rows
    
  def getCell(self, x, y):
    return self.cell[y*self.cols + x]

class Base:
  NO_SOLUTIONS = 0
  UNIQUE_SOLUTION = 1
  MULTIPLE_SOLUTIONS = 2

  def __init__(self, url):
    self.decodeURL(url)
    self.decode()
  
  def solve(self):
    (solution_type, solution) = self._solve()
    return {
      'solutionType': solution_type,
      'solution': solution
    }

  def decodeURL(self, url):
      (self.pid, self.cols, self.rows, self.body, self.pflag) = parseURL(url)
      self.board = Board(self.cols, self.rows)

  def decodeNumber16(self):
      bstr = self.body
      c = 0
      i = 0
      for i in range(len(bstr)):
          ca = bstr[i]
          if include(ca, "0", "9") or include(ca, "a", "f"):
              self.board.cell[c] = int(ca, 16)
          elif ca == "-":
              self.board.cell[c] = int(bstr[i+1,i+1+2], 16)
              i += 2
          elif ca == "+":
              self.board.cell[c] = int(bstr[i+1,i+1+3], 16)
              i += 3
          elif ca == "=":
              self.board.cell[c] = int(bstr[i+1,i+1+3], 16) + 4096
              i += 3
          elif ca == "%":
              self.board.cell[c] = int(bstr[i+1,i+1+3], 16) + 8192
              i += 3
          elif ca == ".":
              self.board.cell[c] = -2
          elif ca >= "g" and ca <= "z":
              c += int(ca,36) - 16
          c += 1
          if c >= len(self.board.cell):
              break
      self.body = self.body[i+1:]

def include(ca, bottom, up):
    return bottom <= ca and ca <= up

def initCell(cols, rows):
    return [None for i in range(cols*rows)]

def initBorder(cols, rows):
    horizontals = [[False for c in range(cols)] for r in range(rows+1)]
    verticals = [[False for r in range(rows)] for c in range(cols+1)]
    return (horizontals, verticals)

def parseURL(url):
    # Translation of parse() in parser.js
    qs = url.find("/", url.find("?"))
    pid = url[url.find("?")+1:qs]
    qdata = url[qs+1:]
    inp = qdata.split("/")
    if inp[0] != "" and not math.isnan(int(inp[0])):
        inp.insert(0, "")
    pflag = inp.pop(0)
    cols = int(inp.pop(0))
    rows = int(inp.pop(0))
    if inp[-1] == "":
        inp.pop()
    body = "/".join(inp)
    if pid == 'ichimaga':
        if "m" in pflag: pid = "ichimagam"
        elif "x" in pflag: pid = "ichimagax"
    elif pid == "icelom":
        if "a" not in pflag: pid = "icelom2"
    elif pid == "pipelink":
        if re.match('[0-9]', body): pid = 'pipelinkr'
    elif pid == "bonsan":
        if "c" not in pflag:
            col = cols
            row = rows
            if re.match('[^0]', body[0:((col-1)*row+4)/5 + (col*(row-1)+4)/5]):
                pid = 'heyabon'
    elif pid == 'kramma':
        if 'c' not in pflag:
            _len = (cols - 1) * (rows - 1)
            cc = 0
            for i in range(len(body)):
                ca = body[i]
                if re.match('\w', ca):
                    cc += int(ca, 36)
                    if (cc < len):
                        pid = 'kramman'
                        break
                elif ca == '.':
                    cc += 36
                if cc >= len:
                    break
    return (pid, cols, rows, body, pflag)