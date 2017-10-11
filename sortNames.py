from difflib import SequenceMatcher

import pandas as pd

def predictName(playerone,playertwo):
    p1 = ""
    p2 = ""
    players = []
    csvdata = pd.read_csv(r'thing.csv', skipinitialspace=True, delimiter=",")

    saved_column = csvdata["Names"]

    for row in saved_column:
        player = row[5:]
        if str(player[0]).islower():
            player = row[4:]
        players.append(player)
    print "Done"

    for i in players:
        m = SequenceMatcher(None, playerone, i)
        ratio = m.ratio()
        print ratio,i
        if ratio > .80:
            p1= i

    for i in players:
        m = SequenceMatcher(None, playertwo, i)
        ratio = m.ratio()
        print ratio,i
        if ratio > .80:
            p2= i
    print(p1,p2)


def playerP(player,player1):
    a = player
    b = player1
    a = a.replace(" ", "-", 1).lower()
    a = a.replace(" ", "", 1)
    b = b.replace(" ", "-").lower()
    print a,b

predictName("Deshone Kizer","Deshaun Watson")




