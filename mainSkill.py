from flask import Flask
from flask_ask import Ask, statement, question
from bs4 import BeautifulSoup
import urllib
import re


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
    msg = "Start or Sit Fantasy is an alexa skill that can help you set your lineup before gameday. Simply give the the name of two NFL players, seperated by and/or, in order to predict the better start. Would you like to try?"
    return question(msg)

@ask.intent("PredictIntent", convert={'playerone':str,'playertwo':str})

def getPrediction(playerone, playertwo):
    try:
        print "{} and {}".format(playerone,playertwo)
        player_names = {"Greg Olson": "Greg Olsen", "le Garrett Blount":"Legarrette Blount","Odell Beckham junior":"Odell Beckham",
                       "Christian MC caffrey":"Christian McCaffrey","jacquizz Rogers":"jacquizz Rodgers"}

        # Replace substrings in line with those in rep
        player_names = dict((re.escape(k), v) for k, v in player_names.iteritems())
        pattern = re.compile("|".join(player_names.keys()))
        a = pattern.sub(lambda m: player_names[re.escape(m.group(0))], playerone)
        b = pattern.sub(lambda m: player_names[re.escape(m.group(0))], playertwo)
        if "Olson" in playerone:
            playerone = "Greg Olsen"
        if "Olson" in playertwo:
            playertwo = "Greg Olsen"
        if "buck" in playerone:
            a = "javorius allen"
        if "buck" in playertwo:
            b = "javorius allen"

        print a
        print b
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

    except Exception as ex:
        return question("I couldn't understand which players you said. Please make sure both players names are said clearly. Can you repeat that?")

if __name__ == "__main__":
    app.run(debug=True)