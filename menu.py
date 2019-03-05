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
        for x in self.savedHeroes:
            self.ownerGame.addPlayer(x,0)

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
                elif line.startswith("NAME="):                   
                    lookName = line.replace("NAME=","")
                    lookName = lookName.strip('\n')
                    lookName = lookName.strip('\t')
                    tp.name = lookName
            elif state == 0:
                if line.startswith("STARTHERO"):
                    tp = Hero()
                    state = 1

    def loadHerosFromFiles(self):
        self.savedHeroes = []
        self.searchFiles()

        
