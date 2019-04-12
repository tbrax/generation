from buff import Buff
import random
class MoveOrder:
    def __init__(self):
        self.am = "INVALID"
        self.type = "INVALID"
        self.triggers = {}
        self.heldValue = 0
        self.tar = "INVALID"

        self.metaInfo = {}

    def checkTriggers(self,user,target):
        totalTrue = True
        for key, value in self.triggers.items():
            if (not user.ownerGame.checkGeneralTrigger(key,value,user,target)):
                totalTrue = False
        user.triggerSave.append(totalTrue)
        return totalTrue

    def selectTargets(self,user,target):
        return user.ownerGame.selectTargets(self.tar,user,target)

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