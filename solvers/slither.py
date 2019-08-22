from claspy import *
from parser import parse
import json

def main(encodedBoard):
  puzzle = parse(encodedBoard)
  height = len(puzzle)
  width = len(puzzle[0])
  horizontalFences = [[BoolVar() for i in range(width)] for j in range(height+1)] 
  verticalFences = [[BoolVar() for i in range(height)] for j in range(width+1)] 
 
  # Require numbers are surrounded by that many fences.
  for y in range(height):
    for x in range(width):
      cell = puzzle[y][x]
      if cell is not None:
        require(horizontalFences[y][x] + horizontalFences[y+1][x] + verticalFences[x][y] + verticalFences[x+1][y] == cell)
  
  # Require that each node has 2 or 0 edges connecting it. This ensures the lines form loop(s) that don't self-intersect.
  for y in range(height+1):
    for x in range(width+1):
      fences = [
        horizontalFences[y][x-1] if x > 0 else None,
        horizontalFences[y][x] if x < width else None,
        verticalFences[x][y-1] if y > 0 else None,
        verticalFences[x][y] if y < height else None,
      ]
      fences = [f for f in fences if f is not None]
      s = fences[0]
      for i in range(1, len(fences)):
        s += fences[i]
      require((s == 2) | (s == 0))
  
  # A grid of atoms for the outside of the loop, proved through flood fill from the a 1 square border padding.
  outside = [[Atom() for i in range(width+2)] for j in range(height+2)]
  for y in range(height+2):
   outside[y][0].prove_if(True)
   outside[y][width+1].prove_if(True)
  for x in range(width+2):
   outside[0][x].prove_if(True)
   outside[height+1][x].prove_if(True)
  for y in range(height+2):
   for x in range(width+2):
     if x-1 >= 0 and y-1 < height and y-1 >= 0:
       outside[y][x].prove_if(outside[y][x-1] & ~verticalFences[x-1][y-1])
     if x < width+1 and y-1 < height and y-1 >= 0:
       outside[y][x].prove_if(outside[y][x+1] & ~verticalFences[x][y-1])
     if y-1 >= 0 and x-1 < width and x-1 >= 0:
       outside[y][x].prove_if(outside[y-1][x] & ~horizontalFences[y-1][x-1])
     if y < height+1 and x-1 < width and x-1 >= 0:
       outside[y][x].prove_if(outside[y+1][x] & ~horizontalFences[y][x-1])
 
  # Requires that each fence has one side outside and one not outside according to the flood fill.
  # This ensures the outside is one connected region.
  for y in range(height+1):
    for x in range(width+1):
      if x < width:
        require(~(horizontalFences[y][x] ^ outside[y][x+1] ^ outside[y+1][x+1]))
      if y < height:
        require(~(verticalFences[x][y] ^ outside[y+1][x] ^ outside[y+1][x+1]))
  
  # Require winding number is 1 so that the inside is one connected region.
  # windingNumber is set to 1000 initially for calculations so that we can subtract without going
  # negative since IntVar's are non-negative
  windingNumber = IntVar(1000)
  for y in range(height+1):
    for x in range(width+1):
      fences = [
        horizontalFences[y][x-1] if x > 0 else None,
        verticalFences[x][y-1] if y > 0 else None,
        horizontalFences[y][x] if x < width else None,
        verticalFences[x][y] if y < height else None,
      ]
      fences = [f if f is not None else False for f in fences]
      windingNumber = cond(outside[y][x] & fences[0] & fences[1], windingNumber - 1, windingNumber)
      windingNumber = cond(~outside[y][x] & fences[0] & fences[1], windingNumber + 1, windingNumber)
      windingNumber = cond(outside[y][x+1] & fences[1] & fences[2], windingNumber - 1, windingNumber)
      windingNumber = cond(~outside[y][x+1] & fences[1] & fences[2], windingNumber + 1, windingNumber)
      windingNumber = cond(outside[y+1][x+1] & fences[2] & fences[3], windingNumber - 1, windingNumber)
      windingNumber = cond(~outside[y+1][x+1] & fences[2] & fences[3], windingNumber + 1, windingNumber)
      windingNumber = cond(outside[y+1][x] & fences[3] & fences[0], windingNumber - 1, windingNumber)
      windingNumber = cond(~outside[y+1][x] & fences[3] & fences[0], windingNumber + 1, windingNumber)
  require(windingNumber == 1004)
  
  solve(quiet=True)
  print json.dumps({'horizontalFences': [[int(str(f)) for f in r] for r in horizontalFences], 'verticalFences': [[int(str(f)) for f in r] for r in verticalFences]})
