from hero import Hero
from move import Move
import random
import json
import os
import copy


class Menu:
    def __init__(self,g):
        self.ownerGame = g
        self.savedHeros = []
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
        self.savedHeros.append(h)

    def startGameCheck(self):
        validTeams = 0
        for idx,x in enumerate(self.queuePlayers):
            c = False
            for y in x:
                c = True
            if c:
                validTeams += 1

        if validTeams < 2:
            return False
        return True

    def addherosToGame(self):
        self.ownerGame.resetVars()
        for idx,x in enumerate(self.queuePlayers):
            for y in x:
                y.ownerGame = 0
                z = copy.deepcopy(y)
                z.ownerGame = self.ownerGame
                self.ownerGame.addPlayer(z,idx)

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
                elif line.startswith("STATS="):
                    eventLine =  line.replace("STATS=","")
                    eventLine = eventLine.strip('\n')
                    eventLine = eventLine.strip('\t')
                    data  = json.loads(eventLine)
                    if isinstance(tp, Hero):
                        tp.loadStatsList(data)

            elif state == 0:
                if line.startswith("STARTHERO"):
                    tp = Hero(self.ownerGame)
                    state = 1

    def loadHerosFromFiles(self):
        self.savedHeros = []
        self.searchFiles()

        
