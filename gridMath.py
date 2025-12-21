def toIndex(x, y):
    return (y - 1) * 10 + (x - 1)
def toX(index):
    return index%10+1
def toY(index):
    return index//10+1
