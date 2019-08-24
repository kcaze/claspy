def parse(encodedBoard):
    parts = encodedBoard.split("/")
    height = parts[0]
    width = parts[1]
    extras = parts[2:-1]
    board = parts[-1]
