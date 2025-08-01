from camelup import camelup
from camelup import calculator
from camelup import cam_to_place
from camelup import place_to_cam
from camelup import find_key_by_value
from camelup import has_min_distance
import copy


def validOperators_getter():
    return ["restart", "calculate", "reset", "help", "start", "show",
            "/restart", "/calculate", "/reset", "/help", "/start", "/show"]

def validCommand_getter():
    return ["blue", "green", "red", "yellow", "white", "pond", "desert", "remove",
                    "blued", "greend", "redd", "yellowd", "whited"]
   
def validAccept(isAccept="YES/NO"):
    A = None
    yes = ["yes", "y", "true", "t", "rolled", "r"]
    no = ["no", "n", "false", "f", "unrolled", "u"]
    if isAccept == "YES":
        A = yes
    elif isAccept == "NO":
        A = no
    elif isAccept == "YES/NO":
        A = yes + no
    return A

def isValidCommand(command):
    isValid = False
    validOperators = validOperators_getter()
    validCommand = validCommand_getter()

    command = command.split(" ")
    if len(command) > 1:
        if command[0] in validCommand[0:8]:
            try:
                n = int(command[1])
                if n>0 and n<=16 and isinstance(n, int):
                    isValid = True
            except Exception as e: print(e)
        
        elif command[0] in validCommand[8:13]:  
             
            if command[1] in validAccept("YES/NO"):
                isValid = True  

    else:
        if command[0] in validOperators:
            isValid = True
    
    return isValid
        
def update_position_toRemove(i, position):
    new_position = copy.deepcopy(position)

    start = 5 * i - 4
    end = 5 * i

    # پیدا کردن خونه‌های اشغال‌شده بین -4 تا 0
    used_positions = set(new_position[color] for color in ["blue", "green", "red", "yellow", "white"])
    available_positions = [pos for pos in range(-4, 1) if pos not in used_positions]

    for color in ["blue", "green", "red", "yellow", "white"]:
        value = new_position.get(color)
        if start <= value <= end:
            if available_positions:
                new_position[color] = available_positions.pop(0)
            else:
                # اگه هیچ جای خالی بین -4 تا 0 نبود، همون مقدار فعلی بمونه یا یه مقدار پیش‌فرض بدیم؟
                new_position[color] = -999  # یا هر مقدار نامعتبر

    new_position["pond"] = [x for x in new_position["pond"] if x != i]
    new_position["desert"] = [x for x in new_position["desert"] if x != i]

    return new_position

def show(position, DiceRolled):
    cams1 = [position["blue"], position["green"], position["red"], position["yellow"], position["white"]]
    cams2 = list(map(place_to_cam, position["desert"]))
    cams3 = list(map(place_to_cam, position["pond"]))
    columns = 17*[""]
    for cam in range(-4, 81):
        i = cam_to_place(cam)
        if cam in cams1:
            n = find_key_by_value(cam, position)
            if n == "blue": columns[i] += "🔵"
            elif n == "green": columns[i] += "🟢"
            elif n == "red": columns[i] += "🔴"
            elif n == "yellow": columns[i] += "🟡"
            elif n == "white": columns[i] += "⚪️"
        elif cam in cams2: columns[i] += "💣"
        elif cam in cams3: columns[i] += "🚀"


    s = "Camels Situation:\n"
    s += f"0️⃣0️⃣: {columns[0]}\n"
    s += "——————————————————\n"
    s += f"0️⃣1️⃣: {columns[1]}\n"
    s += f"0️⃣2️⃣: {columns[2]}\n"
    s += f"0️⃣3️⃣: {columns[3]}\n"
    s += f"0️⃣4️⃣: {columns[4]}\n"
    s += f"0️⃣5️⃣: {columns[5]}\n"
    s += f"0️⃣6️⃣: {columns[6]}\n"
    s += f"0️⃣7️⃣: {columns[7]}\n"
    s += f"0️⃣8️⃣: {columns[8]}\n"
    s += f"0️⃣9️⃣: {columns[9]}\n"
    s += f"1️⃣0️⃣: {columns[10]}\n"
    s += f"1️⃣1️⃣: {columns[11]}\n"
    s += f"1️⃣2️⃣: {columns[12]}\n"
    s += f"1️⃣3️⃣: {columns[13]}\n"
    s += f"1️⃣4️⃣: {columns[14]}\n"
    s += f"1️⃣5️⃣: {columns[15]}\n"
    s += f"1️⃣6️⃣: {columns[16]}\n"
    s += "🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁\n"
    notRolledDices = [key for key, value in DiceRolled.items() if value == False]
    notRolledDicesText = ""
    for dice in notRolledDices:
        if dice == "blue": notRolledDicesText += "🔵"
        elif dice == "green": notRolledDicesText += "🟢"
        elif dice == "red": notRolledDicesText += "🔴"
        elif dice == "yellow": notRolledDicesText += "🟡"
        elif dice == "white": notRolledDicesText += "⚪️"

    s += f"🎲❌ (not rolled dices): {notRolledDicesText}"

    return s

def isValidPosition(position):
    isValid = True
    desertpond_place = position["pond"] + position["desert"]
    if len(desertpond_place) != len(set(desertpond_place)):
        isValid = False
    camels_cam = [position["blue"], position["green"], position["red"], position["yellow"], position["white"]]
    if len(camels_cam) != len(set(camels_cam)):
        isValid = False
    camels_place = [cam_to_place(camel) for camel in camels_cam]
    for i in camels_place:
        if i in desertpond_place:
            isValid = False
            break
    for i in camels_cam:
        if i < -4 or i > 80:
            isValid = False
            break
    for i in range(0, 17):
        isBlank = False
        start = 5*i - 4
        end = 5*i
        for j in range(start, end + 1):
            if isBlank and j in camels_cam:
                isValid = False
                break
            if not(j in camels_cam): isBlank = True
    if has_min_distance(desertpond_place, 1) == False:
        isValid = False 
    return isValid



def api(request, status):

    try:
        request = request.lower()
        validOperators = validOperators_getter()
        validCommand = validCommand_getter()
        if isValidCommand(request):
            answer = ""
            status = copy.deepcopy(status)  # Create a copy of the status to avoid modifying the original

            command = request.split(" ")[0]
            if command in ["calculate", "/calculate"]:
                if isValidPosition(status["position"]):
                    ans = "Calculating the game...\n"
                    camels = camelup(status)
                    ans += "1️⃣ Frist:\n"
                    first = camels["first"]
                    ans += f"🐫🔵: {first['percentage']["blue"]}% ({first['number']["blue"]})\n"
                    ans += f"🐫🟢: {first['percentage']["green"]}% ({first['number']["green"]})\n"
                    ans += f"🐫🔴: {first['percentage']["red"]}% ({first['number']["red"]})\n"
                    ans += f"🐫🟡: {first['percentage']["yellow"]}% ({first['number']["yellow"]})\n"
                    ans += f"🐫⚪️: {first['percentage']["white"]}% ({first['number']["white"]})\n"
                    ans += "—————————————————\n"
                    ans += "2️⃣ Second:\n" 
                    second = camels["second"]
                    ans += f"🐫🔵: {second['percentage']["blue"]}% ({second['number']["blue"]})\n"
                    ans += f"🐫🟢: {second['percentage']["green"]}% ({second['number']["green"]})\n"
                    ans += f"🐫🔴: {second['percentage']["red"]}% ({second['number']["red"]})\n"
                    ans += f"🐫🟡: {second['percentage']["yellow"]}% ({second['number']["yellow"]})\n"
                    ans += f"🐫⚪️: {second['percentage']["white"]}% ({second['number']["white"]})\n"
                    ans += "—————————————————\n"
                    ans += "3️⃣4️⃣5️⃣ Lastest:\n" 
                    last = camels["last"]
                    ans += f"🐫🔵: {last['percentage']["blue"]}% ({last['number']["blue"]})\n"
                    ans += f"🐫🟢: {last['percentage']["green"]}% ({last['number']["green"]})\n"
                    ans += f"🐫🔴: {last['percentage']["red"]}% ({last['number']["red"]})\n"
                    ans += f"🐫🟡: {last['percentage']["yellow"]}% ({last['number']["yellow"]})\n"
                    ans += f"🐫⚪️: {last['percentage']["white"]}% ({last['number']["white"]})\n"
                    answer = ans
                else:
                    answer = "this position is not valid. Please try again. You can restart to set the position again."
            elif command in ["reset", "/reset"]:
                status["DiceRolled"] = {"blue": False,
                                        "green": False,
                                        "red": False,
                                        "yellow": False,
                                        "white": False}  
                answer = "... RESETED ...\n"
            elif command in ["restart", "/restart"]:
                status["position"] = {"blue": 0,
                                    "green": -1,
                                    "red": -2,
                                    "yellow": -3,
                                    "white": -4,
                                    "pond": [],
                                    "desert": []}
                status["DiceRolled"] = {"blue": False,
                                        "green": False,
                                        "red": False,
                                        "yellow": False,
                                        "white": False}
                answer = "... RESTARTED ...\n"
            elif command in ["start", "/start"]:
                answer = "... STARTED ...\n"
            elif command in ["show", "/show"]: pass
            elif command in ["help", "/help"]:
                ans = "You can choose a option berween these items:\n"
                for item in validOperators:
                    if item == "calculate":
                        ans += f"/{item}\n"
                        ans += "- this means calculate the game\n"
                    elif item == "restart":
                        ans += f"/{item}\n"
                        ans += "- this means restart the game\n"
                    elif item == "reset":
                        ans += f"/{item}\n"
                        ans += "- this means reset the Dices to Unrolled\n"
                    elif item == "show":
                        ans += f"/{item}\n"
                        ans += "- this means show the camels position\n"
                    elif item == "help":
                        ans += f"/{item}\n"
                        ans += "- this means show the help\n"
                        
                ans += "\nYou can also use these commands:\n"
                ans += "{color } {a number between 1 to 16}\n"
                ans += "- this means howmany house that camel go\n"
                ans += "{color }D {rolled/unrolled}\n"
                ans += "- this means is that Dice rolled or not\n"
                ans += "{pond/desert} {a number between 1 to 16}\n"
                ans += "- this means which house has pond or desert\n"
                ans += "remove {a number between 1 to 16}\n"
                ans += "- this means remove everythings from that house\n"

                answer = ans
            
            elif command in ["blue", "green", "red", "yellow", "white"]:
                value = int(request.split(" ")[1])
                status["position"] = calculator(status["position"], [(command, value)])
            elif command in ["pond", "desert"]:
                value = int(request.split(" ")[1])
                status["position"] = update_position_toRemove(value, status["position"])
                if command == "pond":
                    status["position"]["pond"].append(int(value))
                else:
                    status["position"]["desert"].append(int(value))
            elif command in ["remove"]:
                value = int(request.split(" ")[1])
                status["position"] = update_position_toRemove(value, status["position"])
            elif command in ["blued", "greend", "redd", "yellowd", "whited"]:
                value = (request.split(" ")[1])
                if value in validAccept("YES"):
                    status["DiceRolled"][command[:-1]] = True
                elif value in validAccept("NO"):
                    status["DiceRolled"][command[:-1]] = False
                else:answer = {"ERROR2! Invalid command. Please try again. Type 'help' for a list of commands."} # ITs not possible to this message showed
            else:
                answer= {"ERROR! Invalid command. Please try again. Type 'help' for a list of commands."} # ITs not possible to this message showed
            
            if command not in ["calculate", "help", "/help"]:
                answer += "\n" + show(status["position"], status["DiceRolled"])

        else:
            answer= "Invalid command. Please try again. Type '/help' for a list of commands."


        return {
            "answer": answer,
            "status": status,
        }
    except Exception as e:
        return {
            "answer": f"CRASHED!!! \nAn error occurred: {str(e)}",
            "status": status,
        }

























# # variables
# request = "start"
# status = {"position": {"blue": 0,
#                  "green": -1,
#                  "red": -2,
#                  "yellow": -3,
#                  "white": -4,
#                  "pond": [],
#                  "desert": []},

#     "DiceRolled": {"blue": False,
#                  "green": False,
#                  "red": False,
#                  "yellow": False,
#                  "white": False}
# }


# while True:
#     response = api(request, status)
#     answer = response["answer"]
#     status = response["status"]
#     print(answer)
#     request = input()
