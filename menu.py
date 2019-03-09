from hero import Hero
from move import Move
import random
import json
import os


class Menu:
    def __init__(self,g):
        self.ownerGame = g
        self.savedHeroes = []
        self.queuePlayers = []
        self.numTeams = 2
        self.menuSetup()

    def menuSetup(self):
        self.loadHerosFromFiles()
        for x in range(self.numTeams):
            e = []
            self.queuePlayers.append(e)

    def searchFiles(self):
        for filename in os.listdir("moveFolder"):
            try:
                self.loadFromFile("moveFolder\\" + filename)
            except Exception as e:
                print("Error loading file " + filename)
                print(e)

    def addHero(self,h):
        self.savedHeroes.append(h)

    def addHeroesToGame(self):
        self.ownerGame.resetVars()
        for idx,x in enumerate(self.queuePlayers):
            for y in x:
                self.ownerGame.addPlayer(y,idx)

    def loadFromFile(self,f):
        file = open(f, "r") 
        state = 0
        tp = 0
        for line in file:
            if state == 1:
                if line.startswith("ENDHERO"): 
                    if isinstance(tp, Hero):
                        self.addHero(tp)
                    tp = 0
                    state = 0
                elif line.startswith("NAME="):                   
                    lookName = line.replace("NAME=","")
                    lookName = lookName.strip('\n')
                    lookName = lookName.strip('\t')
                    tp.name = lookName

                elif line.startswith("MOVES="):
                    eventLine =  line[6:]
                    eventLine = eventLine.strip('\n')
                    eventLine = eventLine.strip('\t')
                    data  = json.loads(eventLine)
                    if isinstance(tp, Hero):
                        tp.loadMovesList(data)

            elif state == 0:
                if line.startswith("STARTHERO"):
                    tp = Hero(self.ownerGame)
                    state = 1

    def loadHerosFromFiles(self):
        self.savedHeroes = []
        self.searchFiles()

        
