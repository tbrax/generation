class Buff:
    def __init__(self,owner,target,myType):
        self.source = owner
        self.myType = myType #BUFF or DEBUFF
        self.target = target
        self.duration = 3
        self.name = ""
        self.countTrigger = "ENDTURN"
        self.do = "USEMOVE"
        self.activate = "EACHCOUNT"
        self.trigger = []
        self.value = []
        self.taken = []
        
    def printSelf(self):
        print(self.name)
        print(self.duration)
        print(self.countTrigger)
        print(self.activate)
        print(self.do)
        print(self.trigger[0])


    def addSelf(self):
        self.target.buffs.append(self)

    def removeSelf(self):
        if self.do == "STAT":
            for idx,x in enumerate(self.trigger):
                v = self.taken[idx]
                self.target.stats[x] += v

        if self in self.target.buffs:
            self.target.buffs.remove(self)

    def startBuff(self):
        self.duration = self.source.parseNum(self.target,self.source,self.duration)
        if self.activate == "STARTCOUNT":
            self.doTrigger()
        self.addSelf()
        self.target.ownerGame.gameAction("TAKE{0}".format(self.myType),self.source,self.target)
        giveStr = "{0} applied to {1}".format(self.name,self.target.getDisplayName())
        self.target.ownerGame.addMessageQ(giveStr,0)

    def endBuff(self):
        if self.activate == "ENDCOUNT":
            self.doTrigger()
        self.removeSelf()

    def countDown(self):

        self.duration -= 1
        if self.activate == "EACHCOUNT":
            self.doTrigger()

        if self.duration <= 0:
            self.endBuff()

    def doTrigger(self):

        if self.do == "USEMOVE":
            for x in self.trigger:
                self.source.activateMove(x,self.target)
        elif self.do == "STAT":
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
        

    def takeAction(self,action):

        if self.countTrigger in action:
            self.countDown()
        if self.activate in action:
            self.doTrigger()
        if self.do == "SLEEP":

            if (action == "SELFALLYTAKEDAMAGE"):
                self.endBuff()

    


