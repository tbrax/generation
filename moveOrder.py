from buff import Buff
import random
class MoveOrder:
    def __init__(self):
        self.am = "DAMAGE"
        self.type = "CRUSH"
        self.triggers = {}
        self.heldValue = 0
        self.tar = "SELECTED"

        self.metaInfo = {}

    def checkTriggers(self,user,target):
        totalTrue = True
        for key, value in self.triggers.items():
            if key == "HIT":
                s = user.parseNum(target,user,value)
                tmpTrue = user.accCheck(target,s)
                if tmpTrue == False:
                    totalTrue = False
                    user.ownerGame.gameAction("MISS",user,target)
            elif key == "RANDOM":
                s = user.parseNum(target,user,value)
                if s < random.randint(0,101):
                    totalTrue = False
            elif key == "PREV":
                if user.triggerSave[-1] == False:
                    totalTrue = False
            elif key == "PREVFALSE":
                if user.triggerSave[-1] == False:
                    totalTrue = True
            elif key == "ALLPREV":
                for x in user.triggerSave:
                    if x == False:
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
            
        user.triggerSave.append(totalTrue)
        return totalTrue

    def selectTargets(self,user,target):
        totalTargets = []
        if self.tar == "SELECTED":
            totalTargets.append(target)
        elif self.tar == "SELF":
            totalTargets.append(user)
        elif self.tar == "ALLALLY":
            for x in user.getAllAlly():
                totalTargets.append(x)
        elif self.tar == "RANDOMALLY":
            totalTargets.append(random.choice(user.getAllAlly()))
        elif self.tar == "RANDOMOTHERALLY":
            totalTargets.append(random.choice(user.getOtherAlly()))
        elif self.tar == "RANDOMENEMY":
            totalTargets.append(random.choice(user.getAllEnemy()))       
        elif self.tar == "OTHERALLY":
            for x in user.getOtherAlly():
                totalTargets.append(x)
        elif self.tar == "ALLENEMY":
            for x in user.getAllEnemy():
                totalTargets.append(x)
        elif self.tar == "ALL":
            for x in user.ownerGame.players:
                for y in x:
                    totalTargets.append(y)
        elif self.tar == "ALLOTHER":
            for x in user.ownerGame.players:
                for y in x:
                    if y != user:
                        totalTargets.append(y)
        elif self.tar == "TARGET":
            for x in user.lastTarget:
                totalTargets.append(x)

        return totalTargets

    def activate(self,user,target):
        totalTargets = self.selectTargets(user,target)
        for x in totalTargets:
            self.activateDo(user,x)

    def activateDo(self,user,target):
        if self.checkTriggers(user,target):
            if self.am == "DAMAGE" or self.am =="HEAL":

                user.dealDamage(target,self.heldValue,self.type,metaData = self.metaInfo)
            elif self.am == "BUFF" or self.am == "DEBUFF":
                b = Buff(user,target,self.am)
                b.name = self.metaInfo["moveName"]
                b.duration = self.metaInfo["buffDuration"]
                b.countTrigger = self.metaInfo["countTrigger"]
                b.do = self.metaInfo["do"]
                b.activate = self.metaInfo["act"]
                b.duration = self.metaInfo["buffDuration"]
                b.trigger.append(self.type)
                b.value.append(self.heldValue)
                b.startBuff()
            elif self.am == "TARGET":
                user.lastTarget.append(target)
                
            
    def addTrigger(self,t):
        if t.startswith("ALWAYS"):
            self.triggers["ALWAYS"] = "1"
        elif t.startswith("PREV"):
            self.triggers["PREV"] = "1"
        elif t.startswith("ALLPREV"):
            self.triggers["ALLPREV"] = "1"
        elif t.startswith("HIT="):
            self.triggers["HIT"] = t[4:]
        elif t.startswith("RANDOM="):
            self.triggers["RANDOM"] = t[7:]
        elif "#<#" or "#>#" or "#e#" in t:
            t0 = t.split("=")
            self.triggers[t0[0]] = t0[1]




    def load(self,data):
        for key, value in data.items():
            if key == "DAMAGE" or key == "HEAL":
                self.am = "DAMAGE"
                for x in value:
                    if x.startswith("AMT="):
                        self.heldValue = x[4:]
                    elif x.startswith("TYPE="):
                        self.type = x[5:].upper()
                        
                    elif x.startswith("TARGET="):
                        self.tar = x[7:]
                    elif x.startswith("CRIT="):
                        self.metaInfo["baseCrit"] = x[5:]
                    elif x.startswith("CRITBONUS="):
                        self.metaInfo["bonusCrit"] = x[10:]
            elif key == "BUFF" or key == "DEBUFF":
                self.am = key
                for x in value:
                    if x.startswith("AMT="):
                        self.heldValue = x[4:]
                    elif x.startswith("TYPE="):
                        self.type = x[5:]
                    elif x.startswith("TARGET="):
                        self.tar = x[7:]
                    elif x.startswith("NAME="):
                        self.metaInfo["moveName"] = x[5:]
                    elif x.startswith("DUR="):
                        self.metaInfo["buffDuration"] = x[4:]
                    elif x.startswith("COUNTTRI="):
                        self.metaInfo["countTrigger"] = x[9:]
                    elif x.startswith("DO="):
                        self.metaInfo["do"] = x[3:]
                    elif x.startswith("ACT="):
                        self.metaInfo["act"] = x[4:]
            elif key == "TARGET":
                self.am = key
                for x in value:
                    if x.startswith("TARGET="):
                        self.tar = x[7:]

            elif key =="TRIGGER":
                for x in value:
                    self.addTrigger(x)