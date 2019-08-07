from hero import Hero
from move import Move
from buff import Buff
from passive import Passive
import random

class scrollText:
    def __init__(self):
        self.text = ""
        self.visible = True
        self.prior = 0
        self.children = []

class Game:
    def __init__(self):
        self.resetVars()
        self.players = []
        self.display = 0

    def resetVars(self):
        
        self.selected = 0
        self.target = 0
        #self.messageDest = 0
        self.messageQueue = []
        self.visibleMessage = []
        self.turnOrder = []
        self.turnCurrent = 0
        self.round = 0
        self.terrain = ["Grave"]
        self.day = 1
        self.dayCount = 6
        
    def checkGeneralTrigger(self,key,value,user,target):
        totalTrue = True
        if key == "HIT":
            s = user.parseNum(target,user,value)
            tmpTrue = user.accCheck(target,s)
            if tmpTrue == False:
                totalTrue = False
                user.ownerGame.gameAction("MISS",user,target)
                target.ownerGame.gameAction("DODGE",target,user)
        elif key == "RANDOM":
            s = user.parseNum(target,user,value)
            if s < random.randint(0,101):
                totalTrue = False
        elif "#<#" in key:
            k = key.replace("#<#","")
            k0 = user.parseNum(target,user,k)
            k1 = user.parseNum(target,user,value)
            if not (k0<k1):
                totalTrue = False
        elif "#>#" in key:
            k = key.replace("#>#","")
            k0 = user.parseNum(target,user,k)
            k1 = user.parseNum(target,user,value)
            if not (k0>k1):
                totalTrue = False
        elif "#e#" in key:
            k = key.replace("#e#","")
            k0 = user.parseNum(target,user,k)
            k1 = user.parseNum(target,user,value)
            if not (k0==k1):
                totalTrue = False
        elif key == "PREV":
            if user.triggerSave[-1] == False:
                totalTrue = False
        elif key == "PREVFALSE":
            if user.triggerSave[-1] != False:
                totalTrue = False
        elif key == "ALLPREV":
            for x in user.triggerSave:
                if x == False:
                    totalTrue = False

        return totalTrue

    def selectTargets(self,tar,user,target):
        totalTargets = []
        if tar == "SELECTED":
            totalTargets.append(target)
        elif tar == "SELF":
            totalTargets.append(user)
        elif tar == "ALLALLY":
            for x in user.getAllAlly():
                totalTargets.append(x)
        elif tar == "RANDOMALLY":
            totalTargets.append(random.choice(user.getAllAlly()))
        elif tar == "RANDOMOTHERALLY":
            totalTargets.append(random.choice(user.getOtherAlly()))
        elif tar == "RANDOMENEMY":
            totalTargets.append(random.choice(user.getAllEnemy()))       
        elif tar == "OTHERALLY":
            for x in user.getOtherAlly():
                totalTargets.append(x)
        elif tar == "ALLENEMY":
            for x in user.getAllEnemy():
                totalTargets.append(x)
            
        elif tar == "ALL":
            for x in user.ownerGame.players:
                for y in x:
                    totalTargets.append(y)
        elif tar == "ALLOTHER":
            for x in user.ownerGame.players:
                for y in x:
                    if y != user:
                        totalTargets.append(y)
        elif tar == "TARGET":
            for x in user.lastTarget:
                totalTargets.append(x)
        elif tar == "TARGETENEMY":
            for x in target.getAllEnemy():
                totalTargets.append(x)
        elif tar == "TARGETALLY":
            for x in target.getAllAlly():
                totalTargets.append(x)
        elif tar == "ALLNOTTARGET":
            for x in user.ownerGame.players:
                for y in x:
                    if y != target:
                        totalTargets.append(y)

        return totalTargets

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
        self.gameAction("STARTGAME",0,0)
        self.calcTurn()

    def endPlayerTurns(self):
        for x in self.players:
            for y in x:
                y.myTurn = False

    def startPlayerTurn(self,player):
        self.endPlayerTurns()
        player.myTurn = True
        self.gameAction("STARTTURN",0,player)

    def endRoundCheck(self):
        if self.turnCurrent >= len(self.turnOrder):
            self.gameAction("ENDROUND",0,0)
            
            self.calcTurn()
            
    def endTurn(self):
        self.gameAction("ENDTURN",self.turnOrder[self.turnCurrent],self.turnOrder[self.turnCurrent])
        
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
        self.round +=1
        self.day += 1
        if self.day > self.dayCount:
            self.day = 1
        self.gameAction("STARTROUND",0,0) 
        self.startPlayerTurn(self.turnOrder[self.turnCurrent])
        

    def gameActionText(self,action,source,target):
        if action == "STARTTURN":
            s = "{0} turn".format(target.getDisplayName())
            self.addMessageQ(s,3)
        elif action == "STARTROUND":
            s = "ROUND {0}".format(self.round)
            self.addMessageQ(s,4)
        elif action == "DIED":
            s = "{0} has died".format(target.getDisplayName())
            self.addMessageQ(s,4)
        elif action == "MISS":
            s = "Miss on {0}".format(target.getDisplayName())
            self.addMessageQ(s,1)
        elif action == "CHANGETERRAIN":
            s = "Terrain changed to {0}".format(self.terrain[0])
            self.addMessageQ(s,1)
        

    def gameAction(self,action,source,target):
        self.checkEnd()
        self.gameActionText(action,source,target)
        for x in self.players:
            for y in x:
                y.takeAction(action,source,target)

    def getPlayerTurn(self):
        return "getTurn not implemented"
    def updateVisibleMessage(self):
        self.visibleMessage = []
        for x in self.messageQueue:
            self.visibleMessage.append(x.text)

    def addMessageQ(self,msg,p):
        t = scrollText()
        t.text = msg
        t.prior = p
        self.messageQueue.append(t)
        self.updateVisibleMessage()
        self.updateDisplay("TEXT")

    def updateDisplay(self,msg):
        if self.display != 0:
            self.display.takeGameMessage(msg)


    def addPlayer(self,p,team):
        p.ownerGame = self
        p.team = team

        if (len(self.players) < team+1):
            tm = []
            tm.append(p)
            self.players.append(tm)
        else:
            self.players[team].append(p)
        p.id = "{0} {1}".format(team,len(self.players[team])-1)

    def makePlayer(self,name,team):
        p = Hero(self)
        p.name = name
        #p.addMove("Punch")
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

        self.addMessageQ(send,0)

    #def addMessage(self,msg):
       
        #self.messageQueue += msg

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

        #self.addMessage(send)

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

    def loadPassive(self,name,user):
        newPassive = Passive(user,name)
        
        return newPassive

    def loadMove(self,name,char):
        
        newMove = Move(name)
        #newMove.name = name.upper()

        newMove.createMove(char)
        if newMove.loaded != 2:
            return 0
        return newMove

    def explainMove(self,name):
        trueName = name.replace("!MOVE ","")

        trueName = trueName.upper()
        newMove = self.loadMove(trueName)
        if newMove == 0:
            self.addMessageQ("The move {0} does not exist".format(trueName),0)
        else:
            self.addMessageQ(newMove.describe(),0)

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