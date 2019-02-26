from move import Move

class Hero:
    def __init__(self):
        self.ownerGame = None
        self.name = "BOB"
        self.displayName = "BOB"
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
            }

        self.typeResist = []
        self.typeDamage = []
        self.exp = 0
        self.level = 1
        self.points = 3
        self.unusedPoints = 3
        self.pointAbilities = []
        self.moves = []
        self.buffs = []
        self.debuffs = []

    def getDisplayName(self):
        return self.name

    def expToLevel(self):
        return self.level * 5

    def dealDamage(self,target,amt,damageType):
        target.takeDamage(self,amt,damageType)

    def takeDamage(self,source,amt,damageType):
        calcAmt = amt

        self.stats["HEALTH"] = self.stats["HEALTH"] - calcAmt

        showAmt = round(calcAmt,1)
        giveStr = "{0} takes {1} {2} damage".format(self.name,showAmt,damageType)
        self.ownerGame.addMessage({giveStr})

    def addMove(self,name):
        found = 0
        for x in self.moves:
            if x.name == name:
                found = 1
        if found == 0:
            newMove = self.ownerGame.loadMove(name)
            if newMove != 0:
                self.moves.append(newMove)
           
    def useMove(self,moveName,target):
        for x in self.moves:
            if x.name == moveName:
                
                x.use(self,target)
            else:
                self.ownerGame.addMessage({"You do not know the move '"+moveName+"' "})

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
