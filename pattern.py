from gridMath import toX, toY


def checkNeighbours(plants, index):
    x, y = toX(index), toY(index)

    # Adjacent (straight)
    if ((x > 1 and plants[index - 1] != " ") or
        (x < 10 and plants[index + 1] != " ") or
        (y > 1 and plants[index - 10] != " ") or
        (y < 10 and plants[index + 10] != " ")):
        return 5

    # Diagonal nearby
    elif ((x > 1 and y > 1 and plants[index - 11] != " ") or
          (x < 10 and y > 1 and plants[index - 9] != " ") or
          (x > 1 and y < 10 and plants[index + 9] != " ") or
          (x < 10 and y < 10 and plants[index + 11] != " ")):
        return 4

    # 2 away straight
    elif ((x > 2 and plants[index - 2] != " ") or
          (x < 9 and plants[index + 2] != " ") or
          (y > 2 and plants[index - 20] != " ") or
          (y < 9 and plants[index + 20] != " ")):
        return 3

    # L-shape
    elif ((x > 1 and y > 2 and plants[index - 21] != " ") or
          (x < 10 and y > 2 and plants[index - 19] != " ") or
          (x > 1 and y < 9 and plants[index + 19] != " ") or
          (x < 10 and y < 9 and plants[index + 21] != " ") or
          (x > 2 and y > 1 and plants[index - 12] != " ") or
          (x < 9 and y > 1 and plants[index - 8] != " ") or
          (x > 2 and y < 10 and plants[index + 8] != " ") or
          (x < 9 and y < 10 and plants[index + 12] != " ")):
        return 2

    # 2 away diagonally
    elif ((x > 2 and y > 2 and plants[index - 22] != " ") or
          (x < 9 and y > 2 and plants[index - 18] != " ") or
          (x > 2 and y < 9 and plants[index + 18] != " ") or
          (x < 9 and y < 9 and plants[index + 22] != " ")):
        return 1

    else:
        return 0


def checkAdjacentP(plants, index):
    x, y = toX(index), toY(index)

    # Check straight adjacent cells for "P"
    if ((x > 1 and plants[index - 1] == "P") or
        (x < 10 and plants[index + 1] == "P") or
        (y > 1 and plants[index - 10] == "P") or
        (y < 10 and plants[index + 10] == "P")):
        return True
    return False


def checkUniqueAdjacent(plants, index):
    x, y = toX(index), toY(index)

    return len({
        plants[i]
        for i, ok in [
            (index - 1,  x > 1),
            (index + 1,  x < 10),
            (index - 10, y > 1),
            (index + 10, y < 10),
        ]
        if ok and plants[i] != " "
    })
