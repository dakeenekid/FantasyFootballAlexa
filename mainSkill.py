from flask import Flask
from flask_ask import Ask, statement, question
from bs4 import BeautifulSoup
import urllib
import pandas as pd
from difflib import SequenceMatcher


app = Flask(__name__)
ask = Ask(app,"/")

@ask.launch
def launch():
    msg = "Welcome to Fantasy Pick or Sit! Which two players are you deciding between?"
    return question(msg)

@ask.intent("ExitIntent")
def exit():
    msg = "Goodbye!"
    return statement(msg)

@ask.intent("YesIntent")
def yesIntent():
    msg = "What are the names of the two fantasy players you need help deciding between?"
    return question(msg)

@ask.intent("HelpIntent")
def help():
    msg = "Start or Sit Fantasy is an alexa skill that can help you set your lineup before gameday. Simply give the the name of two NFL players, seperated by and/or, in order to predict the better start. You cannot compare kickers to anything other than kickers, or this will throw an error. Would you like to try?"
    return question(msg)

@ask.intent("PredictIntent", convert={'playerone':str,'playertwo':str})

def getPrediction(playerone, playertwo):

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

        print "{} and {}".format(p1,p2)
        if p1=="":
            p1 = playerone
        if p2=="":
            p2 = playertwo

        a = p1
        b = p2

        print a
        print b

        if(a=="Alex Smith"):
            a="Alex Smith-sf"

        if(b=="Alex Smith"):
            b = "Alex Smith-sf"
        a = a.replace(" ","-",1).lower()
        a = a.replace(" ","",1)
        b = b.replace(" ","-").lower()

        web = "https://www.fantasypros.com/nfl/start/"+a+"-"+b+".php"
        print web
        site = urllib.urlopen(web)
        # BeautifulSoup object of the HTML code
        soup = BeautifulSoup(site, 'html.parser')
        # From the html, find an h4 attribute that has the type span and the name more
        p1_percent = soup.find("span", attrs={"class":"more"})
        p1_name = str(soup.find("div", attrs={"class":"three columns"}))
        index = p1_name.find("value")
        p1_name = p1_name[index+6:]
        p1_name = p1_name.split(">")

        # Print the price as text, but without the html tags around it. .strip() removes the tags.
        p1_percent = p1_percent.text.strip()
        p1_name = p1_name[0]
        return question(str(p1_name+" is a better start, according to "+p1_percent+" of fantasy experts. Would you like to ask again?"))

    except:
        return question("Sorry, I couldn't understand which players you said. If you are having trouble, please say, help, for more information and instrucitons. Remember, you cannot compare kickers to anything other than kickers")


if __name__ == "__main__":
    app.run(debug=True)