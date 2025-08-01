from tel import validOperators_getter
ans = "You can choose a option berween these items:\n"
for item in validOperators_getter():
    ans += f"/{item}\n"
    if item == "calculate":
        ans += "- this means calculate the game\n"
    elif item == "restart":
        ans += "- this means restart the game\n"
    elif item == "reset":
        ans += "- this means reset the Dices to Unrolled\n"
    elif item == "show":
        ans += "- this means show the camels position\n"
    elif item == "help":
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


print(answer)