from hero import *
from game import *
import wikipedia
import os
Mgame = Game()

def getMsg(m,a):
    send = []
    send += Mgame.takeInput(m,a)
    return send


def main():

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
