from hero import Hero
from move import Move
import random

class scrollText:
    def __init__(self):
        self.text = ""
        self.visible = True
        self.prior = 0
        self.children = []

class Game:
    #def __init__(self):
    #    self.resetVars()

    def resetVars(self):
        self.players = []
        self.selected = 0
        self.target = 0
        #self.messageDest = 0
        self.messageQueue = []
        self.turnOrder = []
        self.turnCurrent = 0
        self.round = 0

    def loadAllHerosFromFiles(self):
        print("Loading all valid heroes")

    def getPlayer(self,team,player):
        return self.players[team][player]

    def resetGame(self):
        self.resetVars()
        #self.makePlayer("Toby",0)
        ##self.makePlayer("Travis",0)
        #self.makePlayer("John",1)
        #self.makePlayer("Jake",1)
        #self.getPlayer(0,0).stats["SPEED"] = 10
        self.startGame()

    def startGame(self):
        self.calcTurn()

    def startPlayerTurn(self,player):
        self.gameAction("STARTTURN",0,player)

    def endRoundCheck(self):
        if self.turnCurrent >= len(self.turnOrder):
            self.gameAction("ENDROUND",0,0)
            
            self.calcTurn()
            
            

    def endTurn(self):
        self.gameAction("ENDTURN",0,0)
        
        self.turnCurrent += 1
        self.endRoundCheck()
        while not self.turnOrder[self.turnCurrent].canFight:
            self.turnCurrent += 1
            self.endRoundCheck()
        if self.turnCurrent != 0:
            self.startPlayerTurn(self.turnOrder[self.turnCurrent])

    def winGame(self,team):
        print("Team " + str(team) + " Wins")

    def endGame(self,teamStatus):
        for idx,x in enumerate(teamStatus):
            if x == False:
                self.winGame(idx)
                

    def checkEnd(self):
        wins = self.checkEndCount()
        count = 0
        for x in wins:
            if x == False:
                count +=1
        if count == 1:
            self.endGame(wins)

    def checkEndCount(self):
        teamsAlive = []
        for x in self.players:
            allDead = True
            for y in x:
                if y.canFight():
                    allDead = False
            teamsAlive.append(allDead)
        return teamsAlive



    def calcTurn(self):
        self.turnCurrent = 0
        self.turnOrder = []
        for x in self.players:
            for y in x:
                self.turnOrder.append(y) 
        self.turnOrder = self.turnOrder = sorted(self.turnOrder, reverse=True,key=lambda v: (v.parseNum(v,v,v.stats["SPEED"]), random.random()))
        self.gameAction("STARTROUND",0,0)
        self.startPlayerTurn(self.turnOrder[self.turnCurrent])
        

    def gameActionText(self,action,source,target):
        if action == "STARTTURN":
            s = "{0} turn".format(target.getDisplayName())
            self.addMessageQ(s,3)
        elif action == "STARTROUND":
            self.round +=1
            s = "ROUND {0}".format(self.round)
            self.addMessageQ(s,4)
        elif action == "DIED":
            self.round +=1
            s = "{0} has died".format(target.getDisplayName())
            self.addMessageQ(s,4)
        

    def gameAction(self,action,source,target):
        self.checkEnd()
        self.gameActionText(action,source,target)
        for x in self.players:
            for y in x:
                y.takeAction(target,action)

    def getPlayerTurn(self):
        return "getTurn not implemented"

    def addMessageQ(self,msg,p):
        print(msg)
        t = scrollText()
        t.text = msg
        t.prior = p
        self.messageQueue.append(t)

    def addPlayer(self,p,team):
        if (len(self.players) < team+1):
            tm = []
            tm.append(p)
            self.players.append(tm)
        else:
            self.players[team].append(p)

    def makePlayer(self,name,team):
        p = Hero()
        p.ownerGame = self
        p.name = name
        p.team = team
        p.addMove("Punch")
        self.addPlayer(p,team)

    def getTeams(self):
        return self.players

    def checkPlayer(self,owner):
        found = 0
        for x in self.players:
            if x.name == owner:
                found = 1
        if found == 0:
            self.makePlayer(owner,0)

    def cmdMe(self,owner):
        self.checkPlayer(owner)
        send = []
        
        for x in self.players:
            if x.name == owner:
                send += x.info()

        self.addMessage(send)

    def addMessage(self,msg):
       
        self.messageQueue += msg

    def help(self):
        send = []
        send += {"Commands:"}
        send += {"!me - lists your character's stats"}
        send += {"!fight - looks for a fight"}

        send += {"!move - Lists all your moves. Give it a move to tell you about it. Ex: !move shotgun or !move 0"}
        send += {"!use - Uses a specified move. Ex: !use shotgun or !use 0"}
        send += {"!inv - Displays your character's inventory"}
        send += {"!status - Shows buffs and debuffs on your character"}
        send += {"!die - You die"}

        self.addMessage(send)

    def useMove(self,move,owner):
        self.checkPlayer(owner)
        trueMove = move.replace("!USE ","")
        if trueMove == "":
            for x in self.players:
                if x.name == owner:
                    x.listMoves()
        else:
            for x in self.players:
                if x.name.upper() == owner.upper():
                    x.useMove(trueMove,x)


    def loadMove(self,name):
        
        newMove = Move()
        newMove.name = name.upper()

        newMove.createMove()
        if newMove.loaded != 2:
            return 0
        return newMove

    def explainMove(self,name):
        trueName = name.replace("!MOVE ","")

        trueName = trueName.upper()
        newMove = self.loadMove(trueName)
        if newMove == 0:
            self.addMessage("The move {0} does not exist".format(trueName))
        else:
            self.addMessage(newMove.describe())

    def takeInput(self,textInput,owner):
        t = textInput.upper()
        self.messageQueue = []
        if t == "!ME":
            self.cmdMe(owner)
        elif t == "!HELP":
            self.help()

        elif t.startswith("!USE"):
            self.useMove(t,owner)

        elif t.startswith("!MOVE"):
            self.explainMove(t)

        return self.messageQueue