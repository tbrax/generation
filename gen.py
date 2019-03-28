
import json
import random
import csv
import math
from collections import defaultdict

import nltk 
from nltk.corpus import wordnet 
class Gen:
    def __init__(self):
        self.name = "man"
        self.keywords = {}
        self.poolItem = {}
        self.poolName = {}
        self.list = {}
        self.statsPlus = {"DAMAGE":0.5, "SPEED":0.6}
        self.statsMinus = {"DAMAGE":0.5, "SPEED":0.6}
        self.typePlus = {}
        self.typeMinus = {}
        self.typeResist = {}
        self.moveMech = {}
        self.totalMech = {}
        self.myRaces = {}
        self.columns = {}
        self.moveName = {}
        self.madeMoves = {}
        

    
    def getSynonyms(self,word):
        synonyms = [] 
        
        for syn in wordnet.synsets(word): 
            for l in syn.lemmas(): 
                synonyms.append(l.name()) 
        return synonyms

    def getAntonyms(self,word):
        antonyms = []      
        for syn in wordnet.synsets(word): 
            for l in syn.lemmas(): 
                if l.antonyms(): 
                    antonyms.append(l.antonyms()[0].name())
        return antonyms



    def loadKeyWords(self):
        columns = defaultdict(list) # each value in each column is appended to a list
        with open("keywords\keyS.txt") as f:
            reader = csv.DictReader(f) # read rows into a dictionary format
            for row in reader: # read a row as {column1: value1, column2: value2,...}
                for (k,v) in row.items(): # go over each column name and value 
                    columns[k].append(v.upper())

        with open("keywords\keyT.txt") as f:
            reader = csv.DictReader(f) # read rows into a dictionary format
            for row in reader: # read a row as {column1: value1, column2: value2,...}
                for (k,v) in row.items(): # go over each column name and value 
                    columns[k].append(v.upper())

        with open("keywords\keyR.csv") as f:
            reader = csv.DictReader(f) # read rows into a dictionary format
            for row in reader: # read a row as {column1: value1, column2: value2,...}
                for (k,v) in row.items(): # go over each column name and value 
                    columns[k].append(v.upper())

        for (k,v) in columns.items():
            for element in v:
                if "+" in element:
                    sp = element.replace("+", "")
                    v.remove(element)
                    columns[k] = v + columns[sp]

        self.columns = columns

    def listToPool(self,listGive):
        l2 = {}
        poolName = {}
        poolItem = {}
        for (k,v) in listGive.items():
            l2[k.upper()] = v   


        columns = self.columns

        for (k,v) in columns.items():
            for row in v:
                if row in l2:
                    poolName[row] = l2[row]
                    if k in poolItem:
                        poolItem[k] = poolItem[k]+l2[row]
                    else:
                        poolItem[k] = l2[row]
        
        self.poolItem = poolItem
        self.poolName = poolName


        
    def splitPool(self):
        self.statsPlus = {}
        self.statsMinus = {}
        for key, value in self.poolItem.items():
            if key.startswith("STATPLUS"):
                s = key.replace("STATPLUS", "")
                self.statsPlus[s] = value
            elif key.startswith("STATMINUS"):
                s = key.replace("STATMINUS", "")
                self.statsMinus[s] = value
            elif key.startswith("TYPEPLUS"):
                s = key.replace("TYPEPLUS", "")
                self.typePlus[s] = value
            elif key.startswith("TYPEMINUS"):
                s = key.replace("TYPEMINUS", "")
                self.typeMinus[s] = value
            elif key.startswith("TYPERESIST"):
                s = key.replace("TYPERESIST", "")
                self.typeResist[s] = value
            elif key.startswith("RACE"):
                s = key.replace("RACE", "")
                self.myRaces[s] = value
            elif key.startswith("STRONGVS"):
                #s = key.replace("STRONGVS", "")
                self.totalMech[key] = value
            elif key.startswith("MECH"):
                #s = key.replace("STRONGVS", "")
                self.totalMech[key] = value

    def calcStats(self):
        retStats = self.statsPlus.copy()
        multN = 50
        for key, value in self.statsMinus.items():
            if key in retStats:
                retStats[key] = retStats[key] - self.statsMinus[key]
            else:
                retStats[key] = -(self.statsMinus[key])
        
        for key, value in retStats.items():
            i = random.randint(50,60)
            retStats[key] *= multN
            retStats[key] *= (1+(i/100))
            retStats[key] = round(retStats[key])
            if key == "MAXHEALTH":
                retStats[key]+=100
                retStats[key] = max(retStats[key],50)
        return retStats

    def calcType0(self):
        retStats = self.typePlus.copy()
        multN = 50
        for key, value in self.typeResist.items():
            if key in retStats:
                retStats[key] = retStats[key] + self.statsMinus[key]
            else:
                retStats[key] = (self.typeResist[key]) 
        for key, value in self.typeMinus.items():
            if key in retStats:
                retStats[key] = retStats[key] - self.statsMinus[key]
            else:
                retStats[key] = -(self.typeMinus[key])       
        for key, value in retStats.items():
            i = random.randint(10,20)
            retStats[key] *= multN
            retStats[key] *= (1+(i/100))
            retStats[key] = min(90,retStats[key])
            retStats[key] = round(retStats[key])
        return retStats

    def calcType1(self):
        retStats = self.typePlus.copy()
        multN = 20

        for key, value in retStats.items():
            i = random.randint(10,20)
            retStats[key] *= multN
            retStats[key] *= (1+(i/100))
            retStats[key] = round(retStats[key])
        return retStats

    def calcRace(self):
        races = []
        for key, value in self.myRaces.items():
            races.append(key)
        return ','.join(races)

    def strChar(self):
        st = ""
        st += "STARTHERO\n"
        st += "NAME=" + self.name + "\n"
        st += "STATS=" + json.dumps(self.calcStats()) + "\n"
        st += "TYPERESIST=" + json.dumps(self.calcType0()) + "\n"
        st += "TYPEDAMAGE=" + json.dumps(self.calcType1()) + "\n"
        st += "TYPERACE=" + self.calcRace() + "\n"
        st += "MOVES=" + json.dumps(self.madeMoves) + "\n"
        st += "ENDHERO\n"
        return st

    def addToName(self,listT):
        for n in self.poolName:
            if n in listT:
                self.moveName.append(n)

    def randomWeightDict(self,d):
        r = random.random()
        total = 0
        for k, v in d.items():
            total += v
        r*=total
        total = 0
        for k, v in d.items():
            total += v
            if r <= total:
                return k
        return False
        
    def createDamage(self):
        damage = 0
        damage += random.randint(10,15)
        if "MECHPLUSDAMAGE" in self.moveMech:
            damage += random.randint(3,6)
        elif "MECHMINUSDAMAGE" in self.moveMech:
            damage -= random.randint(3,6)

        d = ""
        d+=str(damage)
        bonusAttributesList = {}
        for k, v in self.moveMech.items():
            if k.startswith("MECHDAMAGESTAT"):
                stt = k.replace("MECHDAMAGESTAT", "")

        bonusAttributes = self.randomWeightDict(bonusAttributesList)
        return d

    def createTarget(self,mainTarget,isEnemy):
        d = {}


        if (isEnemy):
            d["ALLENEMY"] = 0.5
            d["RANDOMENEMY"] = 0.4
            if (mainTarget == "ENEMY"):
                d["SELECTED"]=1
        else:
            d["ALLALLY"] = 0.3
            d["SELF"] = 0.9
            d["RANDOMALLY"] = 0.2
            d["RANDOMOTHERALLY"] = 0.1
            if (mainTarget == "ALLY"):
                d["SELECTED"]=1

        return self.randomWeightDict(d)
    
    def strBuff(self,mainTarget,isDebuff):
        bType = "BUFF"
        amt = random.randint(15,50)
        namePrefix = "INCREASED_"
        if (isDebuff):
            bType = "DEBUFF"
            amt *= -1
            namePrefix = "DECREASED_"

        rt = {bType:[]}
        rt[bType].append("DO=STAT")
        baseCt = {"DAMAGE":1,"SPEED":1,"ARMOR":1} 
        ct = self.randomWeightDict(baseCt)
        
        tStDict = self.statsPlus.copy()
        for (k,v) in self.totalMech.items():
            if ("MECH"+bType in k):
                sk = k.replace("MECH"+bType,"")
                tStDict[sk] = v
        st = self.randomWeightDict(tStDict)
        if (st != False):
            ct = st

        self.addToName(self.columns["STATPLUS"+ct])
        self.addToName(self.columns["MECH"+bType+ct])

        rt[bType].append("TYPE="+ct)
        

        rt[bType].append("AMT="+str(amt))
        rt[bType].append("TARGET="+self.createTarget(mainTarget,isDebuff))
        rt[bType].append("NAME="+namePrefix+ct)
        rt[bType].append("DUR=3")
        rt[bType].append("COUNTTRI=SELFALLYENDTURN")
        rt[bType].append("ACT=STARTCOUNT")

        return rt

    def strDamage(self,mainTarget):
        rt = {"DAMAGE":[]}
        myType = "CRUSH"

        if len(self.typePlus) > 0:
            myType = self.randomWeightDict(self.typePlus)

        self.addToName(self.columns["TYPEPLUS"+myType])
        rt["DAMAGE"].append("TYPE="+myType)

        rt["DAMAGE"].append("AMT="+self.createDamage())
        rt["DAMAGE"].append("TARGET="+self.createTarget(mainTarget,True))
        calcR = random.randint(0,15)
        calcB = random.randint(0,30)
        rt["DAMAGE"].append("CRIT="+str(calcR))
        rt["DAMAGE"].append("CRITBONUS="+str(calcB))
        return rt

    def strTrigger(self):
        acc = random.randint(70,100)
        t = ["HIT="+str(acc)]
        return t

    def strDo(self,mainTarget):
        self.moveMech = {}
        if len(self.totalMech) > 0:
            nl = random.randint(1,4)
            for x in range(0,nl):
                c = random.choice(list(self.totalMech.keys()))
                self.moveMech[c] = self.totalMech[c]

        rt = "DO="
        myDoChoices = {"DAMAGE":1,"BUFF":0.5,"DEBUFF":0.5}
        myDo = self.randomWeightDict(myDoChoices)
        dc = {}
        if myDo == "DAMAGE":
            dc = self.strDamage(mainTarget)
        elif myDo == "BUFF":
            dc = self.strBuff(mainTarget,False)
        elif myDo == "DEBUFF":
            dc = self.strBuff(mainTarget,True)

        dc["TRIGGER"] = self.strTrigger()

        rt += json.dumps(dc)

        return rt

    def strMove(self):
        self.moveName = []
        rt = "STARTMOVE\n"

       
        dos = []
        nl = random.randint(1,4)
        moveNumberWeights = {"1":1,"2":1,"3":1}
        mainTargetList = {"ALLY":0.3,"ENEMY":1}
        mainTarget = self.randomWeightDict(mainTargetList)
        for x in range(0,nl):
            dos.append(self.strDo(mainTarget))

        rt += "NAME="
        tempName = ""

        nl = random.randint(1,4)

        if len(self.moveName) == 0:
            self.moveName.append("Default_Name")
        for x in range(0,nl):
            newRc = random.choice(self.moveName)
            if (newRc not in tempName):
                if x > 0:
                    tempName += "_"
                tempName += newRc
                
        self.madeMoves[tempName] = 1
        rt += tempName + "\n"

        for x in dos:
            rt += x + "\n"

        rt += "\n"
        rt += "ENDMOVE\n"
        return rt

    def totalChar(self):
        self.madeMoves = {}
        rt = ""
        rt += self.strMove()
        rt += self.strChar()
        
        return rt

    def writeChar(self):
        #self.calc()
        with open("moveFolder\\"+self.name+ ".txt", "w", encoding="utf-8") as f:
            f.write(self.totalChar())

    def calc(self):
        d = {"POwerful":1,"mightY":1.7, "ziPpy":2,"burn":0.5,"cold":0.7,"man":1,"vampire":2}
        
        self.listToPool(d)
        #print(self.poolName)
        self.splitPool()

def main():
    
    ga = Gen()
    ga.loadKeyWords()
    ga.calc()
    #print(ga.columns)
    ga.writeChar()

if __name__== "__main__":
    main()
    #input("Press enter to exit")