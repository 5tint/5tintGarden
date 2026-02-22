from itertools import count

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

def checkAdjacent(plants, index, type):
    x, y = toX(index), toY(index)
    counter = 0

    if type == " ":
        if (x > 1 and plants[index - 1] != " "):
            counter += 1
        if (x < 10 and plants[index + 1] != " "):
            counter += 1
        if (y > 1 and plants[index - 10] != " "):
            counter += 1
        if (y < 10 and plants[index + 10] != " "):
            counter += 1
        return counter

    else:
        if (x > 1 and plants[index - 1] == type):
            counter += 1
        if (x < 10 and plants[index + 1] == type):
            counter += 1
        if (y > 1 and plants[index - 10] == type):
            counter += 1
        if (y < 10 and plants[index + 10] == type):
            counter += 1
        return counter


def checkUniqueAdjacent(plants, index):
    x, y = toX(index), toY(index)

    unique = set()

    # left
    if x > 1 and plants[index - 1] != " ":
        unique.add(plants[index - 1])

    # right
    if x < 10 and plants[index + 1] != " ":
        unique.add(plants[index + 1])

    # up
    if y > 1 and plants[index - 10] != " ":
        unique.add(plants[index - 10])

    # down
    if y < 10 and plants[index + 10] != " ":
        unique.add(plants[index + 10])

    return len(unique)



def checkClusterSize(grid, start_index):
    target = grid[start_index]
    if target is None:
        return 0

    visited = set()
    stack = [start_index]
    size = 0

    while stack:
        i = stack.pop()

        if i in visited:
            continue
        if grid[i] != target:
            continue

        visited.add(i)
        size += 1

        for n in neighbors(i):
            stack.append(n)

    return size

def neighbors(i):
    x = i % 10
    y = i // 10

    result = []

    if x > 0:     result.append(i - 1)   # left
    if x < 9:     result.append(i + 1)   # right
    if y > 0:     result.append(i - 10)  # up
    if y < 9:     result.append(i + 10)  # down

    return result
