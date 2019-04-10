class Passive:
    def __init__(self,owner,myType):
        self.source = owner
        self.myType = myType #BUFF or DEBUFF
        
        self.maxCount = 1
        self.count = 0

        self.name = ""
        self.activate = "ENDTURN"
        self.do = "USEMOVE"
        self.targetChoose = "SELF"

        self.triggers = {}

        self.value = []
        self.taken = []
        self.targets = []
        

    def addSelf(self):
        self.source.passives.append(self)
        self.updateAdd()

    def removeSelf(self):
        if self in self.source.passives:
            self.source.passives.remove(self)

    def updateRemove(self):
        if self.do == "STAT":
            for idx,x in enumerate(self.trigger):
                v = self.taken[idx]
                self.target.stats[x] += v

    def updateAdd(self):
        if self.do == "STAT":
            while len(self.value) < len(self.trigger):
                self.value.append("0")
            while len(self.taken) < len(self.trigger):
                self.taken.append(0)
            for idx,x in enumerate(self.trigger):
                v = self.source.parseNum(self.target,self.source,self.value[idx])
                if (x not in self.target.stats):
                    self.target.stats[x] = 0
                self.target.stats[x] += v
                self.taken[idx] -= v

    def update(self):
        self.updateRemove()
        self.updateAdd()

    def calcValue(self,target):
        v = self.source.parseNum(target,self.source,self.value[0])

    def checkTriggers(self,user,target):
        totalTrue = True
        for key, value in self.triggers.items():
            if (not user.ownerGame.checkGeneralTrigger(key,value,user,target)):
                totalTrue = False
        user.triggerSave.append(totalTrue)
        return totalTrue

    def getAffected(self):
        targets = []
        totalTargets = self.source.ownerGame.selectTargets(self.targetChoose,self.source,self.source)
        for x in totalTargets:
            if self.checkTriggers(self.source,x):
                targets.append(x)
        return targets


    def checkActivate(self):
        self.doTrigger()

    def doTrigger(self):
        
        if self.do == "USEMOVE":
            self.targets = []
            self.targets = self.getAffected()
            for x in self.targets:
                self.source.activateMove(x,self.source)
         
        
    def takeAction(self,action):
        if self.do == "STAT":
            self.update()
        else:
            if self.activate in action:
                self.checkActivate()


    


