from gridMath import toIndex, toX, toY
plants = [" "] * 100
plants[toIndex(2, 2)] = "W"
counter, money, rounds = 0, 0, 1

#Calc and apply monetary gains
def update():
    global money
    revenue = 0
    index = 0
    #Run thru plants
    for plant in plants:

        #Wheat
        if plant == "W":
            revenue += 10
            #Check for potatoes
            if plants[index+1] == "P" or plants[index-1] == "P" or plants[index+10] == "P" or plants[index-10] == "P":
                revenue += 10

        #Carrot
        if plant == "C":
            revenue += 6+1*rounds

        #Potato
        if plant == "P":
            revenue += 8

        #Update the index
        index += 1

    #Add total revenue
    money += revenue

# Mainloop
while counter < 5:

    update()
    print("$", money, " Round:", rounds)
    rounds += 1

    #UI
    print("-" * 41)
    for i in range(0, 100, 10):
        for plant in plants[i:i+10]:
            print("|", plant, end=" ")
        print("|")
        print("-" * 41)


    #Input new Plant
    newplantX = int(input("New Plant X, e.g. 3"))
    newplantY = int(input("New Plant Y, e.g. 3"))
    newplantType = str(input("New Plant Type, e.g. W"))

    #Check for rules request
    if newplantType == "Rules":
        print("W gives 10/r and an extra 10 if round%3==0 and there is atleast 1 adjacent potato")
        print("C gives 7/r + 1 per completed round")
        print("P gives 8/r")
        newplantType = " "

    #Assign new plant to list
    plants[toIndex(newplantX, newplantY)] = newplantType
