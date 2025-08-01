# tools ------------------------------------
from math import ceil
def cam_to_place(num):
    return (ceil(num/5))
def place_to_cam(place):
    return (place*5 - 4)
def has_min_distance(lst, min_dist=1):
    sorted_lst = sorted(lst)
    for i in range(len(sorted_lst) - 1):
        if abs(sorted_lst[i] - sorted_lst[i + 1]) <= min_dist:
            return False
    return True
def find_key_by_value(value, position_dict):
    for key, val in position_dict.items():
        if val == value:
            return key
    return None  # اگر مقدار پیدا نشد
#-------------------------------------------
isReversedBack = False



def conditions_creator(diceRolled):
    notRolledDice = []
    for dice in diceRolled:
        if diceRolled[dice] == False: 
            notRolledDice.append(dice)

    # now we have notRolledDice

    # GPT codes:
    from itertools import permutations, product
    colors = notRolledDice
    dice_values = [1, 2, 3]
    # تمام ترتیب‌های ممکن از رنگ‌ها (چون ترتیب مهمه)
    conditions = []
    for color_order in permutations(colors):
        # تمام حالت‌های ممکن برای تاس‌ها
        for dice_combination in product(dice_values, repeat=len(colors)):
            # چاپ ترکیب رنگ و عدد متناظر
            result = list(zip(color_order, dice_combination))
            conditions.append(result)

    # now we have conditions
    # conditions counter formula: (factorial(len(notRolledDice)) * (3**len(notRolledDice)))

    return conditions

from copy import deepcopy
def calculator(position, condition):

    position = deepcopy(position)

    trapsPlaces = position["pond"] + position["desert"]
    for step in condition:
        diceColor = step[0]
        diceNum = step[1]
        camelsPlaces = [position["blue"], position["green"], position["red"], position["yellow"], position["white"]]

        camelsAbove = []
        j = 1
        while (position[diceColor] + j) in camelsPlaces:
            camelsAbove.append(find_key_by_value(position[diceColor] + j, position))
            j += 1

        futurePlace = cam_to_place(position[diceColor])+diceNum
        isTrapInFuture = futurePlace in trapsPlaces
        if isTrapInFuture:
            if futurePlace in position["pond"]:
                futurePlace += 1
                #go forward----------------------------
                j = 1
                while (futurePlace-1)*5+j in camelsPlaces:
                    j += 1
                camDelta = (futurePlace-1)*5+j - position[diceColor]
                position[diceColor] = position[diceColor] + camDelta
                for above in camelsAbove:
                    position[above] = position[above] + camDelta
                #--------------------------------------
            else:
                futurePlace -= 1
                if not(isReversedBack):
                    #go backward----------------------------
                    l = [5,4,3,2,1]
                    for j in l:
                        if (futurePlace-1)*5+j in camelsPlaces:
                            camDelta = len(camelsAbove)
                            position[find_key_by_value((futurePlace-1)*5+j, position)] = position[find_key_by_value((futurePlace-1)*5+j, position)] + camDelta+1
                    camDelta = (futurePlace-1)*5+1 - position[diceColor]
                    position[diceColor] = position[diceColor] + camDelta
                    for above in camelsAbove:
                        position[above] = position[above] + camDelta
                    #---------------------------------------

        else:
            #go forward----------------------------
            j = 1
            while (futurePlace-1)*5+j in camelsPlaces:
                j += 1
            camDelta = (futurePlace-1)*5+j - position[diceColor]
            position[diceColor] = position[diceColor] + camDelta
            for above in camelsAbove:
                position[above] = position[above] + camDelta
            #--------------------------------------




        for color in ['blue', 'green', 'red', 'yellow', 'white']:
            if position[color] > 80:
                return position  

    #now we have newPosition
    return position
    

def picture_position(position):
    sequence = [
    0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80,
    -1, 4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59, 64, 69, 74, 79,
    -2, 3, 8, 13, 18, 23, 28, 33, 38, 43, 48, 53, 58, 63, 68, 73, 78,
    -3, 2, 7, 12, 17, 22, 27, 32, 37, 42, 47, 52, 57, 62, 67, 72, 77,
    -4, 1, 6, 11, 16, 21, 26, 31, 36, 41, 46, 51, 56, 61, 66, 71, 76
    ]
    s = ""
    for i in sequence:
        n = find_key_by_value(i, position)
        if n == None:
            if (i-5*(i//5)) == 1:
                
                if (i-1)/5+1 in position["pond"]:
                    s += "|  +++  |"
                elif (i-1)/5+1 in position["desert"]:
                    s += "|  ---  |"
                else: s += "|       |"
            else: s += "|       |"
        elif n == "blue": s += "| blue  |"
        elif n == "green":s += "| green |"
        elif n == "red":s += "|  red  |"
        elif n == "yellow":s += "|yellow |"
        elif n == "white":s += "| white |"

        if i >= 76 and i <=80:
            print(s)
            s = ""
    print("|   0   |"+"|   1   |"+"|   2   |"+"|   3   |"+"|   4   |"+"|   5   |"+"|   6   |"+"|   7   |"+"|   8   |"+"|   9   |"+"|  10   |"+"|  11   |"+"|  12   |"+"|  13   |"+"|  14   |"+"|  15   |"+"|  16   |")

from collections import Counter
def percent(List, isLast=False):
    count = Counter(List)
    total = len(List)

    percentage_dict = {}
    number_dict = {}

    for color in ['blue', 'green', 'red', 'yellow', 'white']:
        pct = (count[color] / total) * 100 if color in count else 0
        if isLast:
            pct *= 3
        percentage_dict[color] = round(pct, 2)
        number_dict[color] = count[color]

    return {"percentage": percentage_dict, "number": number_dict}







def camelup(status):
    first = []
    second = []
    last = []
    for condition in conditions_creator(status["DiceRolled"]):
        pos = status["position"]
        future = calculator(pos, condition)
        


        camels = {k: v for k, v in future.items() if k in ['blue', 'green', 'red', 'yellow', 'white']}
        sorted_camels = sorted(camels.items(), key=lambda x: x[1], reverse=True)
    
        first.append([sorted_camels[0][0]][0]) 
        second.append([sorted_camels[1][0]][0])
        for i in [sorted_camels[i][0] for i in range(2, 5)]:
            last.append(i)



    picture_position(status["position"])
    false_colors = [color for color, value in status["DiceRolled"].items() if not value]
    print(false_colors)

    print("First place: ---------------------")
    print(percent(first))
    print("Second place: --------------------")
    print(percent(second))
    print("Last place: ----------------------")
    print(percent(last, True))

    print("===========================================")
    print("===========================================")
    print("====================END====================")
    print("===========================================")
    print("===========================================")
    return({"first": percent(first), 
            "second": percent(second),
            "last": percent(last, True)})
























































# status = {"position": {"blue": 71,
#                  "green": 72,
#                  "red": 73,
#                  "yellow": 74,
#                  "white": 75,
#                  "pond": [16],
#                  "desert": []},

#     "DiceRolled": {"blue": False,
#                  "green": False,
#                  "red": False,
#                  "yellow": False,
#                  "white": False}
# }

# print(camelup(status))
