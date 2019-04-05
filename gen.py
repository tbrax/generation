
import json
import random
import csv
import math
from collections import defaultdict

import nltk 
from nltk.corpus import wordnet 
class Gen:
    def __init__(self):
        self.name = ""
        self.keywords = {}
        self.poolItem = {}
        self.poolName = {}
        self.list = {}
        self.statsPlus = {}
        self.statsMinus = {}
        self.typePlus = {}
        self.typeMinus = {}
        self.typeResist = {}
        self.moveMech = {}
        self.totalMech = {}
        self.myRaces = {}
        self.columns = {}
        self.moveName = {}
        self.madeMoves = {}
        self.artWords = {}
        self.matched = {}
        

    
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
        with open("keywords\\keyS.csv") as f:
            reader = csv.DictReader(f) # read rows into a dictionary format
            for row in reader: # read a row as {column1: value1, column2: value2,...}
                for (k,v) in row.items(): # go over each column name and value 
                    columns[k].append(v.upper())

        with open("keywords\\keyT.csv") as f:
            reader = csv.DictReader(f) # read rows into a dictionary format
            for row in reader: # read a row as {column1: value1, column2: value2,...}
                for (k,v) in row.items(): # go over each column name and value 
                    columns[k].append(v.upper())

        with open("keywords\\keyR.csv") as f:
            reader = csv.DictReader(f) # read rows into a dictionary format
            for row in reader: # read a row as {column1: value1, column2: value2,...}
                for (k,v) in row.items(): # go over each column name and value 
                    columns[k].append(v.upper())

        with open("keywords\\keyM.csv") as f:
            reader = csv.DictReader(f) # read rows into a dictionary format
            for row in reader: # read a row as {column1: value1, column2: value2,...}
                for (k,v) in row.items(): # go over each column name and value 
                    columns[k].append(v.upper())


        addColumns = {}
        for (k,v) in columns.items():
            for element in v:
                if "+" in element:
                    #print(v)
                    sp = element.replace("+", "")                 
                    element = ""
                    if (sp in columns):
                        columns[k] = v + columns[sp]
                    else:
                        print("Cannot find: " + sp)
                    #print(v)
                    #v.remove(element)
        self.columns = columns

        #self.columns.update(addColumns)

    def listToPool(self,listGive):
        l2 = {}
        poolName = {}
        poolItem = {}
        matched = {}
        for (k,v) in listGive.items():
            l2[k.upper()] = v   

        self.artWords = l2
        columns = self.columns

        #print(columns)

        for (k,v) in columns.items():
            for row in v:
                if row in l2:
                    poolName[row] = l2[row]
                    if (row not in matched):
                        matched[row] = []
                    matched[row].append(k)
                    if k in poolItem:
                        poolItem[k] = poolItem[k]+l2[row]
                    else:
                        poolItem[k] = l2[row]
                    
        self.poolItem = poolItem
        self.poolName = poolName
        self.matched = matched
        return matched
        #print(self.poolItem)
        #print(self.poolName)


        
    def splitPool(self):
        self.statsPlus = {}
        self.statsMinus = {}
        bonusStats0 = {"DAMAGE":1,"SPEED":1,"DODGE":1,"ACCURACY":1,"ARMOR":1,"HEAL":1,"LIFESTEAL":1,"MAXHEALTH":1,"CRIT":1}
        
        bonusStats1 = {"DAMAGE":1,"SPEED":1,"DODGE":1,"ACCURACY":1,"MAXHEALTH":1}
        for x in range(3):
            s0 = self.randomWeightDict(bonusStats0)
            self.statsPlus[s0] = random.randint(10,15)
            s1 = self.randomWeightDict(bonusStats1)
            self.statsMinus[s1] = random.randint(10,15)
        
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
                self.totalMech["STRONGVS{0}".format(s)] = value
            elif key.startswith("STRONGVS"):
                #s = key.replace("STRONGVS", "")
                self.totalMech[key] = value
            elif key.startswith("MECH"):
                #s = key.replace("STRONGVS", "")
                self.totalMech[key] = value

        for key,value in self.statsPlus.items():
            while (self.statsPlus[key] < 10):
                self.statsPlus[key] *= 10
        for key,value in self.statsMinus.items():
            while (self.statsMinus[key] < 10):
                self.statsMinus[key] *= 10

    def calcStats(self):
        retStats = self.statsPlus.copy()
        multN = 20
        for key, value in self.statsMinus.items():
            if key in retStats:
                retStats[key] = retStats[key] - self.statsMinus[key]
            else:
                retStats[key] = -(self.statsMinus[key])
        
        bonusMult0 = {  "DAMAGE":0.8,"ARMOR":0.8,"HEAL":1.2,
                        "LIFESTEAL":0.6,"MAXHEALTH":2,"CRITDAMAGE":2
                        }
        for key, value in retStats.items():
            i = random.randint(50,60)
            while(abs(retStats[key])<10):
                retStats[key] *= 10
            retStats[key] *= (1+(i/100))
            if (key in bonusMult0):
                retStats[key] *= bonusMult0[key]
            retStats[key] = round(retStats[key])
            if key == "MAXHEALTH":
                retStats[key]+=100
                retStats[key] = max(retStats[key],50)
        return retStats

    def calcType0(self):
        retStats = self.typePlus.copy()
        multN = 10
        for key, value in self.typeResist.items():
            
            if key in retStats:
                
                retStats[key] = retStats[key] + self.typeResist[key]
            else:
                retStats[key] = (self.typeResist[key]) 
        for key, value in self.typeMinus.items():
            if key in retStats:
                retStats[key] = retStats[key] - self.typeMinus[key]
            else:
                retStats[key] = -(self.typeMinus[key])       
        for key, value in retStats.items():
            self.addToName(self.columns[key])
            i = random.randint(10,20)
            while(abs(retStats[key])<10):
                retStats[key] *= 10
            retStats[key] *= (1+(i/100))
            retStats[key] = min(90,retStats[key])
            retStats[key] = round(retStats[key])
        return retStats

    def calcType1(self):
        retStats = self.typePlus.copy()
        multN = 20

        for key, value in retStats.items():
            i = random.randint(10,20)
            while(abs(retStats[key])<10):
                retStats[key] *= 10
            retStats[key] *= (1+(i/100))
            retStats[key] = round(retStats[key])
        return retStats

    def calcRace(self):
        races = []
        for key, value in self.myRaces.items():
            self.addToName(self.columns[key])
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
        st += "MATCHED=" + json.dumps(self.matched) + "\n"
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
        if "STATPLUSDAMAGE" in self.moveMech:
            damage += random.randint(3,6)
        elif "STATMINUSDAMAGE" in self.moveMech:
            damage -= random.randint(3,6)
        d = ""
        d+=str(damage)
        bonusAttributesList = {"NONE":1}
        for k, v in self.moveMech.items():
            if (k.startswith("STATPLUS") or 
                k.startswith("MECHBUFF") or 
                k.startswith("STRONGVS")):
                bonusAttributesList[k] = v

        bonusAttributes = self.randomWeightDict(bonusAttributesList)
        bonusTx = ""
        if bonusAttributes != False:
            self.addToName(self.columns[bonusAttributes])
            if bonusAttributes.startswith("STATPLUS"):
                r = float(random.randint(50,200)/100)
                stt = bonusAttributes.replace("STATPLUS","")
                bonusTx += "+"+str(r)+"*USER"+stt
            elif bonusAttributes.startswith("MECHBUFF"):
                r = float(random.randint(50,200)/100)
                stt = bonusAttributes.replace("MECHBUFF","")
                bonusTx += "+"+str(r)+"*USER"+stt
            elif bonusAttributes.startswith("STRONGVS"):
                r = float(random.randint(50,200)/100)
                stt = bonusAttributes.replace("STRONGVS","")
                bonusTx += "+"+str(r)+"*TARRACE["+stt+"]"

        d += bonusTx

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

        return self.strCBuff(mainTarget,isDebuff)
    
    def strCBuff(self,mainTarget,isDebuff):
        bType = "BUFF"
        amt = random.randint(15,50)
        namePrefix = "INCREASED_"
        baseCt = {"DAMAGE":1,"SPEED":1,"ARMOR":1,"DODGE":1,"ACCURACY":1,"CRIT":1} 
        if (isDebuff):
            bType = "DEBUFF"
            amt *= -1
            namePrefix = "DECREASED_"
            baseCt["CRITCHANCERESIST"] = 1
            baseCt["CRITDAMAGERESIST"] = 1
        else:
            baseCt["CRITDAMAGE"] = 1
            baseCt["HEAL"] = 1
            baseCt["LIFESTEAL"] = 1

        rt = {bType:[]}
        myDoList = {"STAT":1,"SLEEP":0.1,"STUN":0.06}
        for (k,v) in self.totalMech.items():
            if ("SLEEP" in k):
                myDoList["SLEEP"] = 1
            elif ("STUN" in k):
                 myDoList["STUN"] = 1


        myDo = self.randomWeightDict(myDoList)
        self.addToName(self.columns[myDo])
        if (myDo == "STAT"):
            rt[bType].append("DO=STAT")
            
            ct = self.randomWeightDict(baseCt)
            
            tStDict = self.statsPlus.copy()
            for (k,v) in self.totalMech.items():
                if ("MECH"+bType in k):
                    sk = k.replace("MECH"+bType,"")
                    tStDict[sk] = v
            st = self.randomWeightDict(tStDict)
            if (st != False):
                ct = st
            if (("STATPLUS"+ct) in self.columns):
                self.addToName(self.columns["STATPLUS"+ct])
            elif (("MECH"+bType+ct) in self.columns):
                self.addToName(self.columns["MECH"+bType+ct])

            rt[bType].append("TYPE="+ct)
            dAmt = random.randint(2,4)
            rt[bType].append("NAME="+namePrefix+ct)
            rt[bType].append("AMT="+str(amt))

        elif (myDo == "STUN" or myDo == "SLEEP"):
            dAmt = random.randint(1,3)
            rt[bType].append("NAME="+myDo)
            self.addToName(self.columns["MECH"+myDo])
        

        
        rt[bType].append("TARGET="+self.createTarget(mainTarget,isDebuff))   
        rt[bType].append("DUR="+str(dAmt))
        rt[bType].append("COUNTTRI=SELFALLYENDTURN")
        rt[bType].append("ACT=STARTCOUNT")

        return rt

    def strDamage(self,mainTarget,isHarm=True):
        if (isHarm):
            tp = "DAMAGE"
        else:
            tp = "HEAL"
        rt = {tp:[]}
        dTypes = {"CRUSH":1,"PIERCE":1,"SLASH":1}
        

        if len(self.typePlus) > 0:
            # myType = self.randomWeightDict(self.typePlus)
            dTypes[self.randomWeightDict(self.typePlus)] = 4
        myType = self.randomWeightDict(dTypes)
        self.addToName(self.columns["TYPEPLUS"+myType])

        rt[tp].append("TYPE="+myType)
        if (isHarm):
            rt[tp].append("AMT="+self.createDamage())
        else:
            rt[tp].append("AMT=-1*("+self.createDamage()+")")
        rt[tp].append("TARGET="+self.createTarget(mainTarget,isHarm))
        calcR = random.randint(0,15)
        calcB = random.randint(0,30)
        rt[tp].append("CRIT="+str(calcR))
        rt[tp].append("CRITBONUS="+str(calcB))
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
        myDoChoices = {"DAMAGE":0.7,"BUFF":0.3,"DEBUFF":0.4,"HEAL":0.3}
        myDo = self.randomWeightDict(myDoChoices)
        dc = {}
        if myDo == "DAMAGE":
            dc = self.strDamage(mainTarget,True)
        elif myDo == "BUFF":
            dc = self.strBuff(mainTarget,False)
        elif myDo == "DEBUFF":
            dc = self.strBuff(mainTarget,True)
        elif myDo == "HEAL":
            dc = self.strDamage(mainTarget,False)

        dc["TRIGGER"] = self.strTrigger()

        rt += json.dumps(dc)

        return rt

    def strMove(self):
        self.moveName = []
        rt = "STARTMOVE\n"

       
        dos = []
        nl = random.randint(1,4)
        moveNumberWeights = {"1":1,"2":0.9,"3":0.5,"4":0.1}
        moveNumberChoose = self.randomWeightDict(moveNumberWeights)
        mainTargetList = {"ALLY":0.3,"ENEMY":1}
        mainTarget = self.randomWeightDict(mainTargetList)
        for x in range(0,int(moveNumberChoose)):
            dos.append(self.strDo(mainTarget))

        rt += "NAME="
        

        

        moveNumberWeights = {"2":1,"3":0.9}
        moveNumberChoose = self.randomWeightDict(moveNumberWeights)

        for x in range(int(moveNumberChoose)):
            self.moveName.append(random.choice(list(self.artWords.keys())))
        
        needName = True
        while(needName):
            tempName = ""
            nl = random.randint(1,4)
            for x in range(0,nl):
                newRc = random.choice(self.moveName)
                if (newRc not in tempName):
                    if x > 0:
                        tempName += "_"
                    tempName += newRc
            if (tempName not in self.madeMoves):
                needName = False
                    
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
        moveNumberWeights = {"6":1}
        moveNumberChoose = self.randomWeightDict(moveNumberWeights)
        for x in range(int(moveNumberChoose)):
            rt += self.strMove()
        rt += self.strChar()
        
        return rt

    def writeChar(self):
        #self.calc()
        with open("moveFolder\\"+self.name+ ".txt", "w", encoding="utf-8") as f:
            f.write(self.totalChar())

    def calc(self,d):
        match = self.listToPool(d)
        return match
        #print(self.poolName)
    
       # self.splitPool()

#def main():
    
 #   ga = Gen()
  #  ga.loadKeyWords()
   # ga.calc()
    #print(ga.columns)
    #ga.writeChar()

#if __name__== "__main__":
    #main()
    #input("Press enter to exit")