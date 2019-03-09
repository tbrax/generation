
class MoveOrder:
    def __init__(self):
        self.am = "DAMAGE"
        self.type = "CRUSH"
        self.triggers = {}
        self.heldValue = 0
        self.tar = "SELECTED"

    def checkTriggers(self,user,target):
        totalTrue = True
        for key, value in self.triggers.items():
            if key == "HIT":
                s = user.parseNum(target,user,value)
                tmpTrue = user.accCheck(target,s)
                if tmpTrue == False:
                    totalTrue = False
                    user.ownerGame.gameAction("MISS",user,target)
            elif key == "PREV":
                if user.triggerSave[-1] == False:
                    totalTrue = False
            elif key == "ALLPREV":
                for x in user.triggerSave:
                    if x == False:
                        totalTrue = False
        user.triggerSave.append(totalTrue)
        return totalTrue

    def selectTargets(self,user,target):
        totalTargets = []
        if self.tar == "SELECTED":
            totalTargets.append(target)
        return totalTargets

    def activate(self,user,target):
        totalTargets = self.selectTargets(user,target)
        for x in totalTargets:
            self.activateDo(user,x)

    def activateDo(self,user,target):
        if self.checkTriggers(user,target):
            if self.am == "DAMAGE":
                user.dealDamage(target,self.heldValue,self.type)

    def addTrigger(self,t):
        if t.startswith("ALWAYS"):
            self.triggers["ALWAYS"] = "1"
        elif t.startswith("PREV"):
            self.triggers["PREV"] = "1"
        elif t.startswith("ALLPREV"):
            self.triggers["ALLPREV"] = "1"
        elif t.startswith("HIT="):
            self.triggers["HIT"] = t[4:]

    def load(self,data):
        for key, value in data.items():
            if key == "DAMAGE":
                self.am = "DAMAGE"
                for x in value:
                    if x.startswith("AMT="):
                        self.heldValue = float(x[4:])
                    elif x.startswith("TYPE="):
                        self.type = x[5:]
                    elif x.startswith("TARGET="):
                        self.tar = x[7:]
            elif key =="TRIGGER":
                for x in value:
                    self.addTrigger(x)