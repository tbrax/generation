import json
import os

from moveOrder import MoveOrder 

class Move:
    def __init__(self,name):
        self.name = name
        self.orderList = []
        self.loaded = 0
        self.desc = ""
        
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
                
                if line.startswith("ENDMOVE"): 
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
                        o = MoveOrder()
                        o.load(data)
                        self.orderList.append(o)
                    elif line.startswith("DESC="):                   
                        lookName = line.replace("DESC=","")
                        lookName = lookName.strip('\n')
                        lookName = lookName.strip('\t')
                        self.desc = lookName
            elif state == 0:
                if line.startswith("STARTMOVE"):
                    state = 1


    def searchFiles(self,char):
        try:
            self.loadFromFile("moveFolder\\" + char +".txt")
        except:
            print("Error loading file " + char)

        if self.loaded != 2:
            for filename in os.listdir("moveFolder"):
                try:
                    self.loadFromFile("moveFolder\\" + filename)
                except:
                    print("Error loading file " + filename)
        
    def describe(self):
        d = self.desc
        #for x in self.orderList:
        #    if "do" in x.metaInfo:
        #        if x.metaInfo["do"] == "USEMOVE":
        #            t = x.type
        #           for y in self.metaMoves:
        #                if y.name == t:
        #                    d+= y.describe()
                    
        return d

    def createMove(self,char):    
        self.searchFiles(char)
        

    def use(self,user,target):
        user.triggerSave = []
        user.lastTarget = []
        for x in self.orderList:
            x.activate(user,target)

