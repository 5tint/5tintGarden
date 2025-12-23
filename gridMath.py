def toIndex(x, y):
    return (y - 1) * 10 + (x - 1)
def toX(index):
    return index%10+1
def toY(index):
    return index//10+1
def indexToPos(index, cols, rows, size):
    row = index // cols
    col = index % cols

    start_x = -cols * size / 2
    start_y =  rows * size / 2

    x = start_x + col * size + size / 2
    y = start_y - row * size - size / 2

    return x, y
