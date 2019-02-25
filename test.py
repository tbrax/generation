from hero import *
from game import *
import wikipedia
import os
Mgame = Game()

def getMsg(m,a):
    send = []
    send += Mgame.takeInput(m,a)
    return send

def loadWiki(fname):
    found = 0
    for filename in os.listdir("articles"):
        if filename == fname:
            print("Document already exists")
            found = 1
    if found == 0:
        try:
            wka = wikipedia.page(fname)
            encodedStr = wka.content
            with open("articles\\"+fname + ".txt", "w", encoding="utf-8") as f:
                f.write(encodedStr)

        except wikipedia.exceptions.DisambiguationError as e:
            print(e.options)


def main():
    try:
        mercury = wikipedia.page("Mercury_(Element)")
        print(mercury.content)
    except wikipedia.exceptions.DisambiguationError as e:
        print (e.options)
    
    g = Game()
    while 0==0:
        y = input()
        
        if y.startswith('!'):
            msg = getMsg(y,"trace")
            bigStr = ""
            for idx,x in enumerate(msg):
                bigStr += x
                if idx != len(bigStr)-1:
                   bigStr += "\n"
            print(bigStr)


if __name__== "__main__":
    main()
