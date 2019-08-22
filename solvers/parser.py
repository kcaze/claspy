def isIntString(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def parse(encodedBoard):
  rows = encodedBoard.split("/")
  y = int(rows[0])
  rows = rows[1:]
  if isIntString(rows[0]):
    x = int(rows[0])
    rows = rows[1:]
  else:
    x = y
  rows = rows[0:y]
  return [[int(c) if isIntString(c) else None for c in row.split("_")[:-1]] for row in rows]
