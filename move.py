import json
import os

from moveOrder import MoveOrder 

class Move:
    def __init__(self):
        self.name = "Punch"
        self.orderList = []
        self.loaded = 0

    def loadFromFile(self,f):
        file = open(f, "r") 
        found = 0
        state = 0
        for line in file:
            if line.startswith("STARTMOVE"):
                state = 1
            if state == 1:
                if line.startswith("NAME="): 
                    
                    lookName = line.replace("NAME=","")
                    lookName = lookName.strip('\n')
                    lookName = lookName.strip('\t')
                    if lookName.upper() == self.name.upper():
                        self.loaded = 1
                        found = 1
                if line == "ENDMOVE":
                    found = 0
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

        
            
        for x in self.orderList:
            x.activate(user,target)

