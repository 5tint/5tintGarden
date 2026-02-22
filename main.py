import random
import turtle
from tabnanny import check
import ast

from pattern import checkNeighbours, checkAdjacentP, checkAdjacent, checkUniqueAdjacent, checkClusterSize, neighbors
from gridMath import toX, toY, toIndex, indexToPos
from textures import wheat, potato, carrot, apple, bamboo, vine, blackapple, stoplight, tabasco, godseed
from data import counter, money, rounds, vplants, vmutations, ROWS, COLS, SIZE, gmprompt, getIntInput, getStrInput, gm, getMatchingElements


plants = [" "] * 100



t = turtle.Turtle()
t.speed(0)
t.hideturtle()
stoplightcache = -1
def getRevenue():
    revenue = 0

    for index, plant in enumerate(plants):
        count = plants.count(plant)

        if plant == "W":
            base = 10
            penalty = max(0, count - 10) * 0.7
            value = base - penalty

            if checkAdjacentP(plants, index):
                value += 6

            revenue += max(0, value)

        elif plant == "C":
            base = 6 + (2 * rounds // 3) * round(0.97 ** rounds, 1)
            penalty = max(0, count - 6)  # same as first snippet
            value = base - penalty

            revenue += max(0, value)

        elif plant == "P":
            # from first snippet: potatoes always cost 1
            revenue += -1

        elif plant == "A":
            base = 15 - checkNeighbours(plants, index) * 1.5
            penalty = max(0, count - 4) * 1.5
            value = base - penalty

            revenue += max(0, value)

            if checkAdjacent(plants, index, "A") == 4:
                plants[index] = "BA"

        elif plant == "B":
            base = 9 + checkUniqueAdjacent(plants, index) * 2
            penalty = max(0, count - 5) * 0.4
            value = base - penalty

            revenue += max(0, value)

        elif plant == "V":
            # first snippet logic:
            # cluster_size = clusters.get(index, 1)
            # base = cluster_size * 1.1
            base = checkClusterSize(plants, index) * 1.1
            penalty = max(0, count - 7) * 0.2
            value = base - penalty

            revenue += max(0, value)

        if plants[index] == " ":
            if checkAdjacent(plants, index, "V") == 1:
                if checkAdjacent(plants, index, "B") == 3:
                    if plants.count(" ") % 5 == 0:
                        plants[index] = "TB"

            if checkUniqueAdjacent(plants, index) == 4 and rounds == 25:
                plants[index] = "GS"

            if toX(index) > 2 and toX(index) < 9 and toY(index) > 2 and toY(index) < 9:
                if (plants[toIndex(toX(index)+2, toY(index))] == "W" and
                    plants[toIndex(toX(index)-2, toY(index))] == "W" and
                    plants[toIndex(toX(index), toY(index)-2)] == "W" and
                    plants[toIndex(toX(index), toY(index)+2)] == "W"):
                    plants[index] = "ST"


    return revenue


def gridOD(factor):

    for _ in range(5):
        t.forward(640)
        t.right(90*factor)
        t.forward(64)
        t.right(90*factor)
        t.forward(640)
        t.left(90*factor)
        t.forward(64)
        t.left(90*factor)

def drawPixel(x, y, size, color):

    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(color)
    t.begin_fill()
    for _ in range(4):
        t.forward(size)
        t.right(90)
    t.end_fill()


def drawTexturedTile(tileIndex, texture):
    PIXELS = 16
    pixel_size = SIZE / PIXELS

    # center of the tile
    cx, cy = indexToPos(tileIndex, COLS, ROWS, SIZE)

    # top-left corner of the tile
    start_x = cx
    start_y = cy

    if rounds > 1:
        start_x += 4

    for i, rgb in enumerate(texture):
        row = i // PIXELS
        col = i % PIXELS

        x = start_x + col * pixel_size
        y = start_y - row * pixel_size

        color = tuple(int(c) / 255 for c in rgb.split(", "))
        drawPixel(x, y, pixel_size, color)


def draw():

    t.clear()

    for _ in range(len(plants)):

        t.penup()

        match plants[_]:
            case "W":
                drawTexturedTile(_, wheat)
            case "P":
                drawTexturedTile(_, potato)
            case "C":
                drawTexturedTile(_, carrot)
            case "A":
                drawTexturedTile(_, apple)
            case "B":
                drawTexturedTile(_, bamboo)
            case "V":
                drawTexturedTile(_, vine)
            case "BA":
                drawTexturedTile(_, blackapple)
            case "ST":
                drawTexturedTile(_, stoplight)
            case "TB":
                drawTexturedTile(_, tabasco)
            case "GS":
                drawTexturedTile(_, godseed)


        t.color("black")

    x, y = indexToPos(0, COLS, ROWS, SIZE)

    t.penup()
    t.goto(x, y)
    t.setheading(0)
    t.pendown()

    gridOD(1)

    t.forward(640)

    for __ in range(2):
        t.left(90)
        t.forward(640)

    t.left(90)

    gridOD(-1)


# Whole process to add a new plant and display the UI for it
def addPlant():
    global rounds
    # Print current money and round number for reference
    print("$", money, " Round:", rounds)

    # Flags to check if user input is valid
    xcheck = False
    ycheck = False
    tcheck = False
    ccheck = False

    # Loop until valid X, Y, and plant type are chosen
    while xcheck == False or ycheck == False or tcheck == False or ccheck == False:

        while ccheck == False:
            # Get valid X coordinate
            while xcheck == False:
                newplantX = getIntInput("New Plant X, e.g. 3:")

                # Check if input is in the allowed range
                if newplantX < 11 and newplantX > 0:
                    xcheck = True
                else:
                    print("Input coords 1-10")

            # Get valid Y coordinate
            while ycheck == False:
                newplantY = getIntInput("New Plant Y, e.g. 3:")

                # Check if input is in the allowed range
                if newplantY < 11 and newplantY > 0:
                    ycheck = True
                else:
                    print("Input coords 1-10")

            if plants[toIndex(newplantX, newplantY)] == " ":
                ccheck = True
            else:
                print("Choose an empty tile")
                xcheck = False
                ycheck = False

        # Get valid plant type
        while tcheck == False:
            newplantType = getStrInput("New Plant type, e.g. W")

            # Check if plant type is valid
            if newplantType.upper() in vplants:
                tcheck = True

            elif newplantType.lower() == "scores":
                print("Highscores:")
                with open("scores.txt", "r") as file:
                    print(file.read(), end="")

            else:
                print("You have to choose one of these plants: ", vplants)


        print("W gives 10/r and an extra 6 if there is atleast 1 adjacent potato")
        print("C gives 7/r + 1 per completed round")
        print("P gives 0/r")
        print("A gives more money the further it is from other plants, up to 15 and at least 7.5")
        print("B gives 9 + 2 per unique neighbour")
        print("V gives 4 + 0.8 per cluster size")

    # Assign new plant to the list at the correct index
    plants[toIndex(newplantX, newplantY)] = newplantType.upper()


gmcheck = False
while gmcheck == False:
    gm = getStrInput(gmprompt)
    gm = gm.upper()
    if gm == "CLASSIC" or gm == "SHORT" or gm == "INSANE" or gm == "MARATHON" or gm == "WILDERNESS":
        gmcheck = True
print("W gives 10/r and an extra 6 if there is atleast 1 adjacent potato")
print("C gives 7/r + 1 per completed round")
print("P gives 0/r")
print("A gives more money the further it is from other plants, up to 15 and at least 7.5")
print("B gives 9 + 2 per unique neighbour")
print("V gives 4 + 0.8 per cluster size")

with open("scores.txt", "r+") as file:
    lines = file.readlines()

line_6 = lines[5].strip()  # line index 5 = line 6
obtainedMutations = ast.literal_eval(line_6)
print(getMatchingElements(obtainedMutations, vmutations))

print(len(obtainedMutations), "/4 Mutations unlocked")
if gm == "CLASSIC":
    while rounds < 16:

        money += getRevenue()
        turtle.tracer(0)
        draw()
        turtle.update()
        addPlant()
        if rounds % 7 == 0:
            print("Second Turn, round%7 == 0")
            turtle.tracer(0)
            draw()
            turtle.update()
            addPlant()
        rounds += 1

if gm == "SHORT":
    while rounds < 11:

        money += getRevenue()
        turtle.tracer(0)
        draw()
        turtle.update()
        addPlant()
        if rounds % 7 == 0:
            print("Second Turn, round%7 == 0")
            turtle.tracer(0)
            draw()
            turtle.update()
            addPlant()
        rounds += 1

if gm == "INSANE":
    while rounds < 16:

        money += getRevenue()
        turtle.tracer(0)
        draw()
        turtle.update()
        addPlant()
        print("Second Turn, its INSANE mode!!!!!!!!!")
        turtle.tracer(0)
        draw()
        turtle.update()
        addPlant()
        rounds += 1

if gm == "MARATHON":
    while rounds < 31:

        money += getRevenue()
        if rounds % 2 == 1:
            print("Planting time!")
            turtle.tracer(0)
            draw()
            turtle.update()
            addPlant()
        else:
            print("Not planting time, wait for the next round :)b")
        rounds += 1

if gm == "WILDERNESS":
    while rounds < 15:

        rcheck = False
        while rcheck == False:
            x = random.randint(1, 10)
            y = random.randint(1, 10)
            if plants[toIndex(x, y)] == " ":
                rcheck = True
        plants[toIndex(x, y)] = vplants[random.randint(0, 5)]
        turtle.tracer(0)
        draw()
        turtle.update()
        money += getRevenue()


        addPlant()
        turtle.tracer(0)
        draw()
        turtle.update()
        rounds += 1

with open("scores.txt", "r+") as file:
    lines = file.readlines()

    # Ensure the file has enough lines (for each game mode)
    while len(lines) < 5:
        lines.append("\n")

    # Update the correct line based on the game mode
    if gm == "CLASSIC":
        lines[0] = f"CLASSIC: {money}\n"
    elif gm == "SHORT":
        lines[1] = f"SHORT: {money}\n"
    elif gm == "INSANE":
        lines[2] = f"INSANE: {money}\n"
    elif gm == "MARATHON":
        lines[3] = f"MARATHON: {money}\n"
    elif gm == "WILDERNESS":
        lines[4] = f"WILDERNESS: {money}\n"


money += getRevenue()


with open("scores.txt", "r+") as file:
    lines = file.readlines()

    # Ensure the file has enough lines (for each game mode)
    while len(lines) < 4:
        lines.append("\n")

    # Print current score
    print(f"Your score: {money}")

    # Check and update score based on the game mode
    if gm == "CLASSIC":
        current_score = int(lines[0].split(":")[1].strip()) if lines[0].strip() else 0
        print(f"Your highscore in CLASSIC: {current_score}$")
        if money > current_score:
            lines[0] = f"CLASSIC: {money}\n"
            print(f"Your new highscore in CLASSIC is {money}$")
    elif gm == "SHORT":
        current_score = int(lines[1].split(":")[1].strip()) if lines[1].strip() else 0
        print(f"Your highscore in SHORT: {current_score}$")
        if money > current_score:
            lines[1] = f"SHORT: {money}\n"
            print(f"Your new highscore in SHORT is {money}$")
    elif gm == "INSANE":
        current_score = int(lines[2].split(":")[1].strip()) if lines[2].strip() else 0
        print(f"Your highscore in INSANE: {current_score}$")
        if money > current_score:
            lines[2] = f"INSANE: {money}\n"
            print(f"Your new highscore in INSANE is {money}$")
    elif gm == "MARATHON":
        current_score = int(lines[3].split(":")[1].strip()) if lines[3].strip() else 0
        print(f"Your highscore in MARATHON: {current_score}$")
        if money > current_score:
            lines[3] = f"MARATHON: {money}$\n"
            print(f"Your new highscore in MARATHON is {money}$")
    elif gm == "WILDERNESS":
        current_score = int(lines[4].split(":")[1].strip()) if lines[3].strip() else 0
        print(f"Your highscore in WILDERNESS: {current_score}$")
        if money > current_score:
            lines[4] = f"WILDERNESS: {money}$\n"
            print(f"Your new highscore in WILDERNESS is {money}$")

    # Write the updated lines to the file if the score was updated
    file.seek(0)
    file.writelines(lines)

with open("scores.txt", "r") as f:
    lines = f.readlines()

# 6th line → index 5
list_line = lines[5].strip()

# Turn the text into a real list
listtemp = ast.literal_eval(list_line)

# Add your string
for element in plants:
    if element == "BA" or element == "ST" or element == "TB" or element == "GS":
        if element not in obtainedMutations:
            obtainedMutations.append(element)

# Write it back as plain text
lines[5] = str(obtainedMutations) + "\n"

with open("scores.txt", "w") as f:
    f.writelines(lines)

print(money)
