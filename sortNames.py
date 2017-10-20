from difflib import SequenceMatcher
from bs4 import BeautifulSoup
import pandas as pd
import urllib


def predictName(playerone,playertwo):
    p1 = ""
    p2 = ""
    players = []
    ratios1 = []
    ratios2 = []
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
        n = SequenceMatcher(None, playertwo, i)
        ratio1 = m.ratio()
        ratio2 = n.ratio()
        ratios1.append(ratio1)
        ratios2.append(ratio2)
    p1 = players[ratios1.index(max(ratios1))]
    p2 = players[ratios2.index(max(ratios2))]
    print p1,p2


def playerP(player,player1):
    a = player
    b = player1
    a = a.replace(" ", "-", 1).lower()
    a = a.replace(" ", "", 1)
    b = b.replace(" ", "-").lower()
    print a,b

def webGet(playerone,playertwo):
    p1 = ""
    p2 = ""
    try:

        players = []
        ratios1 = []
        ratios2 = []
        csvdata = pd.read_csv(r'thing.csv', skipinitialspace=True, delimiter=",")

        saved_column = csvdata["Names"]

        for row in saved_column:
            player = row[5:]
            if str(player[0]).islower():
                player = row[4:]
            players.append(player)

        for i in players:
            m = SequenceMatcher(None, playerone, i)
            n = SequenceMatcher(None, playertwo, i)
            ratio1 = m.ratio()
            ratio2 = n.ratio()
            ratios1.append(ratio1)
            ratios2.append(ratio2)
        p1 = players[ratios1.index(max(ratios1))]
        p2 = players[ratios2.index(max(ratios2))]

        print "{} and {}".format(p1, p2)
        if p1 == "":
            p1 = playerone
        if p2 == "":
            p2 = playertwo

        a = p1
        b = p2

        print a
        print b

        if (a == "Alex Smith"):
            a = "Alex Smith-sf"

        if (b == "Alex Smith"):
            b = "Alex Smith-sf"
        a = a.replace(" ", "-", 1).lower()
        a = a.replace(" ", "", 1)
        b = b.replace(" ", "-").lower()

        web = "https://www.fantasypros.com/nfl/start/" + a + "-" + b + ".php"
        print web
        site = urllib.urlopen(web)
        # BeautifulSoup object of the HTML code
        soup = BeautifulSoup(site, 'html.parser')
        # From the html, find an h4 attribute that has the type span and the name more
        p1_percent = soup.find("span", attrs={"class": "more"})
        p1_name = str(soup.find("div", attrs={"class": "three columns"}))
        index = p1_name.find("value")
        p1_name = p1_name[index + 6:]
        p1_name = p1_name.split(">")

        # Print the price as text, but without the html tags around it. .strip() removes the tags.
        p1_percent = p1_percent.text.strip()
        p1_name = p1_name[0]
        print str(p1_name + " is a better start, according to " + p1_percent + " of fantasy experts. Would you like to ask again?")
    except:
        print "you fucking failed bro"

webGet("kfls;hf", "ipoepwr")




