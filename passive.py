import os
import json

class Passive:
    def __init__(self,owner,name):
        self.source = owner   
        self.maxCount = 0
        self.count = 0
        self.name = name
        self.activate = "INVALID"
        self.do = "INVALID"
        self.targetChoose = "INVALID"
        self.triggers = {}
        self.value = []
        self.taken = []
        self.targets = []
        self.addSelf()
        self.desc = ""
        self.loaded = 0
        

    def addSelf(self):
        self.createPassive()
        self.source.passives.append(self)
        #self.updateAdd()

    def removeSelf(self):
        if self in self.source.passives:
            self.source.passives.remove(self)

    def updateRemove(self):
        self.taken = []
        self.targets = []

    def updateAdd(self):
        self.targets = []
        self.targets = self.getAffected()
        for x in self.targets:
            self.statAdd(x)

    def statAdd(self,p):
        takenUser = []
        for x in self.value:
            v = self.source.parseNum(p,self.source,x)
            takenUser.append(v)
        self.taken.append(takenUser)

    def changeStat(self,p,value,stat):
        print("Changing")


    def update(self):
        self.updateRemove()
        self.updateAdd()

    def loadPassive(self,dat):
        if ("TYPE" in dat):
            self.do = dat["TYPE"]
        if ("ACTIVATE" in dat):
            self.activate = dat["ACTIVATE"]
        if ("TARGET" in dat):
            self.targetChoose = dat["TARGET"]
        if ("TRIGGERS" in dat):
            self.triggers = dat["TRIGGERS"]
        if ("VALUE" in dat):
            self.value = dat["VALUE"]
        if ("COUNT" in dat):
            self.maxCount = int(dat["COUNT"])

    def loadFromFile(self,f):
        file = open(f, "r") 
        found = 0
        state = 0
        for line in file:  
            if state == 1:
                if line.startswith("NAME="): 
                    
                    lookName = line.replace("NAME=","")
                    lookName = lookName.strip('\n')
                    lookName = lookName.strip('\t')
                    if lookName.upper() == self.name.upper():
                        self.loaded = 1
                        found = 1
                
                if line.startswith("ENDPASSIVE"): 
                    found = 0
                    state = 0
                    if self.loaded == 1:
                        self.loaded = 2
                if self.loaded == 1:
                    if line.startswith("DO="):
                        eventLine =  line[3:]
                        eventLine = eventLine.strip('\n')
                        eventLine = eventLine.strip('\t')
                        data  = json.loads(eventLine)
                        self.loadPassive(data)

                    elif line.startswith("DESC="):                   
                        lookName = line.replace("DESC=","")
                        lookName = lookName.strip('\n')
                        lookName = lookName.strip('\t')
                        self.desc = lookName
            elif state == 0:
                if line.startswith("STARTPASSIVE"):
                    state = 1

    def searchFiles(self):
        
        for filename in os.listdir("moveFolder"):
            try:
                self.loadFromFile("moveFolder\\" + filename)
            except:
                print("Error loading file " + filename)

    def createPassive(self):    
        self.searchFiles()

    def checkTriggers(self,user,target):
        totalTrue = True
        for key, value in self.triggers.items():
            if (not user.ownerGame.checkGeneralTrigger(key,value,user,target)):
                totalTrue = False
        #user.triggerSave.append(totalTrue)
        return totalTrue

    def getAffected(self):
        targets = []
        totalTargets = self.source.ownerGame.selectTargets(self.targetChoose,self.source,self.source)
        for x in totalTargets:
            if self.checkTriggers(self.source,x):
                targets.append(x)
        return targets


    def checkActivate(self):
        self.count+=1
        if (self.count >= self.maxCount):
            self.count = 0
            self.doTrigger()

    def doTrigger(self):
        if self.do == "USEMOVE":
            self.targets = []
            self.targets = self.getAffected()
            for x in self.targets:
                if x.canFight():
                    for y in self.value:
                        msg = "{0} activated {1}".format(self.source.getDisplayName(),y)
                        self.source.ownerGame.addMessageQ(msg,1)
                        x.activateMove(y,x)
         
        
    def takeAction(self,action):
        if self.do == "STAT":
            self.update()
        elif self.do == "TYPE":
            if self.activate in action:

                self.checkActivate()


    


