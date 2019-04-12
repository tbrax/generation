from move import Move
from passive import Passive
import random
from math import *
import re
import os
class Hero:
    def __init__(self,g):
        self.ownerGame = g
        self.name = "BOB"
        self.displayName = "BOB"
        self.life = "ALIVE"
        self.team = 0
        self.stats ={
            "HEALTH": 100,
            "MAXHEALTH": 100,
            "DAMAGE": 0,
            "SPEED": 0,
            "CRIT": 0,
            "CRITDAMAGE": 30,
            "CRITRESIST": 0,
            "CRITDAMAGERESIST": 0,
            "ARMOR": 0,
            "ACCURACY": 0,
            "DODGE": 0,
            "HEAL": 0,
            "LIFESTEAL": 0,
            }

        self.typeResist = {}
        self.typeDamage = {}
        self.typeRace = []
        self.exp = 0
        self.level = 1
        self.points = 3
        self.unusedPoints = 3
        self.pointAbilities = []
        self.moves = []
        self.metaMoves = []
        self.buffs = []
        self.myTurn = False
        self.lastTarget = []
        self.id = 0
        self.typeSave = {"LASTDEAL":"CRUSH","LASTTAKE":"CRUSH"}
        self.passives = []
        


    def writeSelf(self):
        t = "STARTHERO\n"
        ##file = open("moveFolder\\" + filename, "w")
        t += "ENDHERO"
        return t

        
    def accCheck(self,target,baseAcc):
        i = random.randint(0,101)
        check = baseAcc + self.stats["ACCURACY"] - target.stats["DODGE"]
        return check > i

    def parseNum(self,target,source,strValue):
        if isinstance(strValue, float) or isinstance(strValue, int) or strValue.isdigit():
            return float(strValue)
        
        s = strValue

        ##############
        rf = s.find("RANDOM")
        if rf != -1:
            myNum = ""
            rCount = rf+7
            while s[rCount] != "]" and rCount < len(s):
                myNum += s[rCount]
                rCount += 1
            s = s[:rf] + str(random.randint(0,int(myNum))) + s[rCount+1:]
        ##############
        rf = s.find("TARRACE")
        if rf != -1:
            myRace = ""
            rCount = rf+8
            while s[rCount] != "]" and rCount < len(s):
                myRace += s[rCount]
                rCount += 1
            rNum = "0"
            if myRace.upper() in (name.upper() for name in target.typeRace):
                rNum = "1"
            s = s[:rf] + rNum + s[rCount+1:]
        #############
        rf = s.find("USERRACE")
        if rf != -1:
            myRace = ""
            rCount = rf+9
            while s[rCount] != "]" and rCount < len(s):
                myRace += s[rCount]
                rCount += 1
            rNum = "0"
            if myRace.upper() in (name.upper() for name in source.typeRace):
                rNum = "1"
            s = s[:rf] + rNum + s[rCount+1:]
        ####################


        ####
        s = s.replace("USERHEALTHHIGH", str(source.stats["HEALTH"]/source.stats["MAXHEALTH"]))
        s = s.replace("TARHEALTHHIGH", str(target.stats["HEALTH"]/target.stats["MAXHEALTH"]))
        s = s.replace("USERHEALTHLOW", str(1-(source.stats["HEALTH"]/source.stats["MAXHEALTH"])))
        s = s.replace("TARHEALTHLOW", str(1-(target.stats["HEALTH"]/target.stats["MAXHEALTH"])))
        ######
        s = s.replace("TURN", str(self.ownerGame.round))
        s = s.replace("USERHEALTH", str(source.stats["HEALTH"]))
        s = s.replace("TARHEALTH", str(target.stats["HEALTH"]))
        s = s.replace("USERMAXHEALTH", str(source.stats["MAXHEALTH"]))
        s = s.replace("TARMAXHEALTH", str(target.stats["MAXHEALTH"]))
        s = s.replace("USERDAMAGE", str(source.stats["DAMAGE"]))
        s = s.replace("TARDAMAGE", str(target.stats["DAMAGE"]))
        s = s.replace("USERSPEED", str(source.stats["SPEED"]))
        s = s.replace("TARSPEED", str(target.stats["SPEED"]))
        s = s.replace("USERCRIT", str(source.stats["CRIT"]))
        s = s.replace("TARCRIT", str(target.stats["CRIT"]))
        s = s.replace("USERCRITDAMAGE", str(source.stats["CRITDAMAGE"]))
        s = s.replace("TARCRITDAMAGE", str(target.stats["CRITDAMAGE"]))
        s = s.replace("USERCRITRESIST", str(source.stats["CRITRESIST"]))
        s = s.replace("TARCRITRESIST", str(target.stats["CRITRESIST"]))
        s = s.replace("USERCRITDAMAGERESIST", str(source.stats["CRITDAMAGERESIST"]))
        s = s.replace("TARCRITDAMAGERESIST", str(target.stats["CRITDAMAGERESIST"]))
        s = s.replace("USERARMOR", str(source.stats["ARMOR"]))
        s = s.replace("TARARMOR", str(target.stats["ARMOR"]))
        s = s.replace("USERACCURACY", str(source.stats["ACCURACY"]))
        s = s.replace("TARACCURACY", str(target.stats["ACCURACY"]))
        s = s.replace("USERDODGE", str(source.stats["DODGE"]))
        s = s.replace("TARDODGE", str(target.stats["DODGE"]))
        s = s.replace("USERHEAL", str(source.stats["HEAL"]))
        s = s.replace("TARHEAL", str(target.stats["HEAL"]))
        s = s.replace("USERLIFESTEAL", str(source.stats["LIFESTEAL"]))
        s = s.replace("TARLIFESTEAL", str(target.stats["LIFESTEAL"]))


        f = eval(s) 

        return float(f)

    def getDisplayName(self):
        if self.id == 0:
            return self.name
        return self.name + " " + str(self.id)


    def takeAction(self, action, source, target):
        actionStr = ""
        if source != 0:
            if source == self:
                actionStr += "SELF"
            else:
                actionStr += "OTHER"
            if source.team == self.team:
                actionStr += "ALLY"
            else:
                actionStr += "ENEMY"
        else:
            if action == "STARTGAME":
                self.startGame()
        finalStr = actionStr + action
        self.checkAction(finalStr)

    def startGame(self):
        self.life = "ALIVE"
        self.stats["HEALTH"] = self.stats["MAXHEALTH"]

    def checkAction(self,action):
        for x in self.buffs:
            x.takeAction(action)
        for x in self.passives:
            x.takeAction(action)
        

    def loadMovesList(self,data):
        for key, value in data.items():
            self.addMove(key)
    
    def loadStatsList(self,data):
        for key, value in data.items():
            self.stats[key] = value

    def loadPassiveList(self,data):
        for key, value in data.items():
            p = Passive(self,key)

    def loadTypeDamageList(self,data):
        for key, value in data.items():
            self.typeDamage[key] = value

    def loadTypeRaceList(self,data):
        self.typeRace = data.split(",")

    def loadTypeResistList(self,data):
        for key, value in data.items():
            self.typeResist[key] = value

    def expToLevel(self):
        return self.level * 5

    def textHealth(self):

        h0 = round(self.stats["HEALTH"],1)
        h1 = round(self.stats["MAXHEALTH"],1)
        giveStr = "{0} / {1} health".format(h0,h1)
        return giveStr
        
    def parseType(self,target,source,damageType):

        if (damageType == "LASTDEAL" or damageType == "LASTTAKE"):
            damageType = self.typeSave[damageType]

        if (damageType not in self.typeResist):
            self.typeResist[damageType] = 0
        if (damageType not in self.typeDamage):
            self.typeDamage[damageType] = 0
        return damageType

    def canFight(self):
        if self.life == "ALIVE":
            return True
        elif self.life == "UNDEAD":
            if self.stats["HEALTH"] > 0:
                return True
        return False

    def canUseMove(self):
        totalTrue = True
        for x in self.buffs:
            if x.do == "STUN":
                totalTrue = False
            elif x.do == "SLEEP":
                totalTrue = False

        return totalTrue

    def die(self):
        self.ownerGame.gameAction("DIED",self,self)
        self.life = "DEAD"
        
    def checkHealth(self):
        
        if self.life == "ALIVE":
            if self.stats["HEALTH"] <= 0:
                self.die()

        if self.stats["HEALTH"] <= 0:
                self.stats["HEALTH"] = 0
                
    def getAllAlly(self):
        get = []
        for x in self.ownerGame.players:
            for y in x:
                if y.team == self.team:
                    get.append(y)
        return get
    
    def getAllEnemy(self):
        get = []
        for x in self.ownerGame.players:
            for y in x:
                if (y.team != self.team):
                    get.append(y)
        return get

    def getOtherAlly(self):
        get = []
        for x in self.ownerGame.players:
            for y in x:
                if y.team == self.team and y != self:
                    get.append(y)
        return get


    def armorCalc(self,source,amt):
        am = (max(10,100 - self.stats["ARMOR"]))/100
        amt2 = amt * am
        return amt2

    def doesCrit(self,target,base):
        i = random.randint(0,101)
        n = self.parseNum(target,self,base)
        n += self.stats["CRIT"]
        n -= target.stats["CRITRESIST"]
        return i < n

    def doLifeSteal(self,target,amt,damageType):

        tam = amt*(self.stats["LIFESTEAL"]/100)
        if tam > 0:
            self.takeHeal(tam,False)
                #takeHeal(self,amt,damageTypeC,dc,metaData)

    def dealDamage(self,target,amt,damageType, metaData = {}):
        if "baseCrit" not in metaData:
            metaData["baseCrit"] = "0"
        if "bonusCrit" not in metaData:
            metaData["bonusCrit"] = "0"

        amt = self.parseNum(target,self,amt)

        
        damageTypeC = self.parseType(target,self,damageType)
        amt = amt * float(max(((100+self.typeDamage[damageTypeC])/100),0))
        dc = self.doesCrit(target,metaData["baseCrit"])
        if amt > 0:
            amt = float(amt) * float((100+self.stats["DAMAGE"])/100)
        self.typeSave["LASTDEAL"] = damageTypeC
        target.takeDamage(self,amt,damageTypeC,dc,metaData)
        self.ownerGame.gameAction("DEALDAMAGE",self,target)

    def calcCrit(self,source,amt,metaData):
        bc = source.parseNum(self,source,metaData["bonusCrit"])
        bonus = ((float(source.stats["CRITDAMAGE"]) + float(bc))/100) * float(amt)
        bonus = bonus * (max(100-self.stats["CRITDAMAGERESIST"],0))/100
        return bonus


    def dealHeal(self,target,amt,damageType, metaData = {}):
        if "baseCrit" not in metaData:
            metaData["baseCrit"] = "0"
        if "bonusCrit" not in metaData:
            metaData["bonusCrit"] = "0"
        amt = self.parseNum(target,self,amt)
        amt = float(amt) * float((100+self.stats["HEAL"])/100)
        ##amt * (1+(self.stats["HEAL"]/100))
        damageTypeC = self.parseType(target,self,damageType)
        amt = amt * float(max(((100+self.typeDamage[damageTypeC])/100),0))
        dc = self.doesCrit(target,metaData["baseCrit"])
        target.takeHeal(amt,dc)
        self.ownerGame.gameAction("DEALHEAL",self,target)

    def takeHeal(self,amt,crit):
        if amt < 0:
            self.stats["HEALTH"] -= amt * (1+(self.stats["HEAL"]/100))
            if self.stats["HEALTH"] > self.stats["MAXHEALTH"]:
                self.stats["HEALTH"] = self.stats["MAXHEALTH"]
            showAmt = -round(amt,1)
            if crit:
                giveStr = "{0} critical heals for {1}".format(self.getDisplayName(),showAmt)
            else:
                giveStr = "{0} heals for {1}".format(self.getDisplayName(),showAmt)
                #self.ownerGame.addMessage({giveStr})
            self.ownerGame.addMessageQ(giveStr,0)
            self.ownerGame.gameAction("TAKEHEAL",self,self)

    def takeDamage(self,source,amt,damageType,crit,metaData = {}):
        calcAmt = self.parseNum(self,source,amt)
        damT = self.parseType(self,source,damageType)
        if crit:
            calcAmt = calcAmt + self.calcCrit(source,amt,metaData)
        if calcAmt > 0:
            calcAmt = float(calcAmt) * float((100-self.typeResist[damT])/100)

        if calcAmt > 0:
            calcAmt = self.armorCalc(source,calcAmt)
            self.stats["HEALTH"] = self.stats["HEALTH"] - calcAmt
            self.typeSave["LASTTAKE"] = damT
            showAmt = round(calcAmt,1)
            if crit:
                giveStr = "{0} takes {1} critical {2} damage".format(self.getDisplayName(),showAmt,damageType.upper())
            else:
                giveStr = "{0} takes {1} {2} damage".format(self.getDisplayName(),showAmt,damageType.upper())
            #self.ownerGame.addMessage({giveStr})
            self.ownerGame.addMessageQ(giveStr,0)
            self.ownerGame.gameAction("TAKEDAMAGE",source,self)
            source.doLifeSteal(self,calcAmt,damageType)
        elif calcAmt < 0:
            self.takeHeal(calcAmt,crit)

        self.checkHealth()

    def addMove(self,name):
        found = 0
        for x in self.moves:
            if x.name == name:
                found = 1
        if found == 0:
            newMove = self.ownerGame.loadMove(name)
            if newMove != 0:
                self.moves.append(newMove)

    def addMoveMeta(self,name):
        found = 0
        for x in self.metaMoves:
            if x.name == name:
                found = 1
        if found == 0:
            newMove = self.ownerGame.loadMove(name)
            if newMove != 0:
                self.metaMoves.append(newMove)

    def activateMove(self,moveName,target):
        moveName = moveName.upper()
        found = False
        for x in self.moves:
            if x.name.upper() == moveName.upper():
                found = True
                x.use(self,target)
        if not found:
            self.addMoveMeta(moveName)
            for x in self.metaMoves:
                if x.name.upper() == moveName.upper():
                    x.use(self,target)
            

    def playMsg(self,msg):
        print(msg)

    def useMove(self,moveName,target):
        if self.myTurn:
            if self.canFight():
                if self.canUseMove():
                    for x in self.moves:
                        if x.name == moveName: 
                            msg = self.getDisplayName() + " used " + moveName + " on " + target.getDisplayName()
                            self.ownerGame.addMessageQ(msg,1)
                            self.activateMove(moveName,target)
                            self.ownerGame.gameAction("USEMOVE",self,target)
                else:
                    self.playMsg("{0} cannot use moves".format(self.getDisplayName()))
            else:
                self.playMsg("{0} cannot fight".format(self.getDisplayName()))
        else:
            self.playMsg("It is not {0} turn".format(self.getDisplayName()))
        
        

    def moveList(self):
        return self.moves

    def getMoveByName(self,name):
        for x in self.moves:
            if x.name == name:
                return x
        return False

    def listMoves(self):
        self.ownerGame.addMessage({"Moves known by {0}:".format(self.name)})
        for x in self.moves:
            self.ownerGame.addMessage({"{0}".format(x.name)})



    def info(self):
        send = []
        showHp = round(self.stats["HEALTH"],1)
        showMhp = round(self.stats["MAXHEALTH"],1)

        send += {"{0}: {1}/{2}".format(self.name,showHp,showMhp)}
        send += {"Level: {0}".format(self.level)}
        return send
