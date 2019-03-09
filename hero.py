from move import Move
import random
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
            "DAMAGE": 100,
            "SPEED": 0,
            "CRIT": 0,
            "CRITDAMAGE": 50,
            "CRITRESIST": 0,
            "CRITDAMAGERESIST": 0,
            "ARMOR": 0,
            "ACCURACY": 0,
            "DODGE": 0,
            }

        self.typeResist = {}
        self.typeDamage = {}
        self.exp = 0
        self.level = 1
        self.points = 3
        self.unusedPoints = 3
        self.pointAbilities = []
        self.moves = []
        self.buffs = []
        self.debuffs = []
        self.myTurn = False

    def accCheck(self,target,baseAcc):
        i = random.randint(0,101)
        check = baseAcc + self.stats["ACCURACY"] - target.stats["DODGE"]
        return check > i

    def parseNum(self,target,source,strValue):
        return float(strValue)

    def getDisplayName(self):
        return self.name


    def takeAction(self, source, action):
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
        finalStr = actionStr + action
        self.checkAction(finalStr)

    def checkAction(self,action):
        x = 0
        

    def loadMovesList(self,data):
        for key, value in data.items():
            self.addMove(key)

    def expToLevel(self):
        return self.level * 5

    def dealDamage(self,target,amt,damageType):
        target.takeDamage(self,amt,damageType)

    def textHealth(self):
        giveStr = "{0} / {1} health".format(self.stats["HEALTH"],self.stats["MAXHEALTH"])
        return giveStr
        
    def parseType(self,target,source,damageType):
        if (damageType not in self.typeResist):
            self.typeResist[damageType] = 1.0
        return damageType

    def canFight(self):
        if self.life == "ALIVE":
            return True
        return False

    def die(self):
        self.life = "DEAD"
        self.ownerGame.gameAction("DIED",self,self)

    def checkHealth(self):
        if self.stats["HEALTH"] <= 0:
                self.stats["HEALTH"] = 0
        if self.life == "ALIVE":
            if self.stats["HEALTH"] <= 0:
                self.die()
                

    def takeDamage(self,source,amt,damageType):
        calcAmt = self.parseNum(self,source,amt)
        dam = self.parseType(self,source,damageType)

        calcAmt = calcAmt * float(self.typeResist[dam])
        self.stats["HEALTH"] = self.stats["HEALTH"] - calcAmt

        showAmt = round(calcAmt,1)
        giveStr = "{0} takes {1} {2} damage".format(self.name,showAmt,damageType)
        #self.ownerGame.addMessage({giveStr})
        self.ownerGame.addMessageQ(giveStr,0)

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

    def activateMove(self,moveName,target):
        for x in self.moves:
            if x.name == moveName:
                x.use(self,target)


    def useMove(self,moveName,target):
        if self.myTurn == True:
            for x in self.moves:
                if x.name == moveName: 
                    msg = self.getDisplayName() + " used " + moveName + " on " + target.getDisplayName()
                    self.ownerGame.addMessageQ(msg,1)
                    self.activateMove(moveName,target)
                else:
                    self.ownerGame.addMessage({"You do not know the move '"+moveName+"' "})
        else:
            print("It is not " + self.getDisplayName() + " turn")
        
        

    def moveList(self):
        return self.moves

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
