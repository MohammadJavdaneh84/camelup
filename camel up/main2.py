from camelup import camelup

status = {"position": {"blue": 0,
                 "green": -2,
                 "red": -3,
                 "yellow": -1,
                 "white": 81,
                 "pond": [],
                 "desert": []},

    "DiceRolled": {"blue": False,
                 "green": False,
                 "red": False,
                 "yellow": False,
                 "white": False}
}

print(camelup(status))