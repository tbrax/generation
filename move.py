import json
import os

from moveOrder import MoveOrder 

class Move:
    def __init__(self):
        self.name = "Punch"
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
                elif line.startswith("DESC="):                   
                    lookName = line.replace("DESC=","")
                    lookName = lookName.strip('\n')
                    lookName = lookName.strip('\t')
                    self.desc = lookName
                if line.startswith("ENDMOVE"): 
                    found = 0
                    state = 0
                    if self.loaded == 1:
                        self.loaded = 2
                if found == 1:
                    if line.startswith("DO="):
                        eventLine =  line[3:]
                        eventLine = eventLine.strip('\n')
                        eventLine = eventLine.strip('\t')
                        data  = json.loads(eventLine)
                        o = MoveOrder()
                        o.load(data)
                        self.orderList.append(o)
            elif state == 0:
                if line.startswith("STARTMOVE"):
                    state = 1


    def searchFiles(self):
        
        for filename in os.listdir("moveFolder"):
            try:
                self.loadFromFile("moveFolder\\" + filename)
            except:
                print("Error loading file " + filename)
        
    def describe(self):
        return "Move"

    def createMove(self):    
        self.searchFiles()
        

    def use(self,user,target):
        user.triggerSave = []
        for x in self.orderList:
            x.activate(user,target)

