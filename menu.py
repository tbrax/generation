from hero import Hero
from move import Move
from tf import tf
from gen import Gen
import random
import json
import os
import copy
import heapq


class Menu:
    def __init__(self,g):
        self.ownerGame = g
        self.savedHeros = []
        self.queuePlayers = []
        self.numTeams = 2
        self.loadWiki = []
        self.menuSetup()
        self.display = 0
        self.matched = {}
        self.numWords = 30
        self.heroNames = []
        


    def menuSetup(self):
        self.loadHerosFromFiles()
        for x in range(self.numTeams):
            e = []
            self.queuePlayers.append(e)

    def loadArticle(self,art):
        if (art != ""):
            newTf = tf()
            newTf.computeText(art)
            
            if (newTf.loaded == "LOADED"):
                self.loadWiki.append(newTf)
            elif (newTf.loaded == "DISAMBIG"):
                if self.display != 0:
                    self.display.disWindow(newTf.options)

        #self.genHero()
    def clearHero(self):
        self.matched = {}
        self.loadWiki = []

    def genHero(self):
        #print("g0")
        t4 = {}
        for t in self.loadWiki:
            # t = self.loadWiki[0]  
            t3 = sorted(t.t2, key=t.t2.get, reverse=True)[:self.numWords] 
            for x in t3:
                t4[x] = t.t2[x]
        #print("g1")
        #print(t4)
        #t3 = heapq.nlargest(10, t.t2, key=t.t2.get)
        #d = {"POwerful":1,"mightY":1.7, "ziPpy":2,"burn":0.5,"cold":0.7,"man":1,"vampire":2}
        ga = Gen()
        n = ""
        for idx,x in enumerate(self.loadWiki):
            if idx != 0:
                n+="-"
            n+= x.name
        #print("g2")
        ga.name = n
        ga.loadKeyWords()
        self.matched = ga.calc(t4)
        #print("g3")

        ga.splitPool()
        #print("g4")
        ga.writeChar()
        #print("g5")
        self.searchFiles()
        #print("g6")

    def addName(self):
        self.heroNames.append("")

    def searchFiles(self):
        self.savedHeros = []
        for filename in os.listdir("moveFolder"):
            #self.loadFromFile("moveFolder\\" + filename)
            try:
                self.loadFromFile("moveFolder\\" + filename)
            except Exception as e:
                print("Error loading menu file " + filename)
                print(e)
                #print("k")

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
                elif line.startswith("PASSIVE="):
                    eventLine =  line.replace("PASSIVE=","")
                    eventLine = eventLine.strip('\n')
                    eventLine = eventLine.strip('\t')
                    data  = json.loads(eventLine)
                    if isinstance(tp, Hero):
                        tp.loadPassiveList(data)
                elif line.startswith("TYPEDAMAGE="):
                    eventLine =  line.replace("TYPEDAMAGE=","")
                    eventLine = eventLine.strip('\n')
                    eventLine = eventLine.strip('\t')
                    data  = json.loads(eventLine)
                    if isinstance(tp, Hero):
                        tp.loadTypeDamageList(data)
                elif line.startswith("TYPERESIST="):
                    eventLine =  line.replace("TYPERESIST=","")
                    eventLine = eventLine.strip('\n')
                    eventLine = eventLine.strip('\t')
                    data  = json.loads(eventLine)
                    if isinstance(tp, Hero):
                        tp.loadTypeResistList(data)
                elif line.startswith("TYPERACE="):
                    eventLine =  line.replace("TYPERACE=","")
                    eventLine = eventLine.strip('\n')
                    eventLine = eventLine.strip('\t')
                    if isinstance(tp, Hero):
                        tp.loadTypeRaceList(eventLine)

            elif state == 0:
                if line.startswith("STARTHERO"):
                    tp = Hero(self.ownerGame)
                    state = 1

    def loadHerosFromFiles(self):
        self.savedHeros = []
        self.searchFiles()

        
