
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
        #self.list = {}
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
        self.moveLine = ""
        self.moveDesc = []
        self.needMove = []
        self.bonusMult0 =   { 
                            "DAMAGE":0.8,"ARMOR":0.8,"HEAL":1.2,
                            "LIFESTEAL":0.6,"MAXHEALTH":2,"CRITDAMAGE":2,
                            "DODGE":0.5,"ACCURACY":0.6
                            }
        

    
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
                self.statsPlus[key] = random.randint(10,35)
        for key,value in self.statsMinus.items():
                self.statsMinus[key] = random.randint(10,35)

    def calcStats(self):
        retStats = self.statsPlus.copy()
        multN = 20
        for key, value in self.statsMinus.items():
            if key in retStats:
                retStats[key] = retStats[key] - self.statsMinus[key]
            else:
                retStats[key] = -(self.statsMinus[key])
        
        
        for key, value in retStats.items():
            while(abs(retStats[key])<10):
                retStats[key] = random.randint(15,40)
            if (key in self.bonusMult0):
                retStats[key] *= self.bonusMult0[key]

            retStats[key] = round(retStats[key])
            if key == "MAXHEALTH":
                retStats[key]+=100
                retStats[key] = max(retStats[key],50)
        return retStats

    def calcType0(self):
        #retStats = self.typePlus.copy()
        retStats = {}
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
            while(abs(retStats[key])<10):
                retStats[key] = random.randint(10,20)
            #retStats[key] *= (1+(i/100))
            retStats[key] = min(90,retStats[key])
            retStats[key] = round(retStats[key])
        return retStats

    def calcType1(self):
        retStats = self.typePlus.copy()
        multN = 20

        for key, value in retStats.items():
            while(abs(retStats[key])<10):
                retStats[key] = random.randint(10,20)
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
    
    def addToDesc(self,add):
        self.moveLine+=add

    def moveLineDown(self):
        self.moveDesc.append(self.moveLine)
        self.moveLine = ""

    def createDamage(self):
        damage = 0
        damage += random.randint(8,22)
        d = ""
        d+=str(damage)
        self.addToDesc("{0} ".format(d))

        bonusAttributesList = {"NONE":1,"AMTRANDOM":0.1,"AMTTURN":0.06}
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
                stt = bonusAttributes.replace("STATPLUS","")
                r = float(random.randint(30,100)/100)
                if (stt in self.bonusMult0):
                    stt *= 1/self.bonusMult0[stt]
                bonusTx += "+"+str(r)+"*USER"+stt
                self.addToDesc("plus {0} * the user's {1} ".format(r,stt))

            elif bonusAttributes.startswith("MECHBUFF"):
                stt = bonusAttributes.replace("MECHBUFF","")
                r = float(random.randint(30,100)/100)
                if (stt in self.bonusMult0):
                    stt *= 1/self.bonusMult0[stt]
                bonusTx += "+"+str(r)+"*USER"+stt
                self.addToDesc("plus {0} * the user's {1} ".format(r,stt))

            elif bonusAttributes.startswith("STRONGVS"):
                r = float(random.randint(50,150)/10)
                stt = bonusAttributes.replace("STRONGVS","")
                bonusTx += "+"+str(r)+"*TARRACE["+stt+"]"
                self.addToDesc("plus {0} if the target is a {1} ".format(r,stt))

            elif bonusAttributes.startswith("AMTRANDOM"):
                r = random.randint(0,15)
                bonusTx += "+RANDOM[{0}]".format(r)
                self.addToDesc("plus a random amount from 0 to {0} ".format(r))

            elif bonusAttributes.startswith("AMTTURN"):
                r = float(random.randint(50,90)/100)
                bonusTx += "+{0}*TURN".format(r)
                self.addToDesc("plus {0} *  the current game round".format(r))

            elif bonusAttributes.startswith("AMTUSERLOW"):
                r = random.randint(0,10)
                bonusTx += "+{0}*USERHEALTHLOW".format(r)
                self.addToDesc("plus up to {0}, depending on how low the user's health is ".format(r))

            elif bonusAttributes.startswith("AMTUSERHIGH"):
                r = random.randint(0,10)
                bonusTx += "+{0}*USERHEALTHHIGH".format(r)
                self.addToDesc("plus up to {0}, depending on how high the user's health is ".format(r))

            elif bonusAttributes.startswith("AMTTARGETLOW"):
                r = random.randint(0,10)
                bonusTx += "+{0}*TARHEALTHLOW".format(r)
                self.addToDesc("plus up to {0}, depending on how low the targets's health is ".format(r))

            elif bonusAttributes.startswith("AMTTARGETHIGH"):
                r = random.randint(0,10)
                bonusTx += "+{0}*TARHEALTHHIGH".format(r)
                self.addToDesc("plus up to {0}, depending on how high the target's health is ".format(r))

            

        d += bonusTx

        return d

    def createTarget(self,mainTarget,isEnemy):
        d = {}
        if (mainTarget == "SELF"):
            d["SELF"]=1
        elif (mainTarget == "SELECTED"):
            d["SELECTED"]=1
        else:
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

        ts = self.randomWeightDict(d)
        self.addToDesc("targeting {0} ".format(ts))
        return ts

    def strBuff(self,mainTarget,isDebuff,mtype="STAT",sc=1):
        if (mtype=="STAT"):
            return self.strSBuff(mainTarget,isDebuff,sc)
        elif (mtype=="OVERTIME"):
            return self.strOBuff(mainTarget,isDebuff,sc)



    def strOBuff(self,mainTarget,isDebuff,sc=1):
        bType = "BUFF"
        if (isDebuff):
            bType = "DEBUFF"

        amt = random.randint(5,12)*sc
        rt = {bType:[]}
        myDoList = {"OVERTIME":1}
        myDo = self.randomWeightDict(myDoList)

        if(myDo == "OVERTIME"):
            rt[bType].append("DO=USEMOVE")
            nname = "{0}{1}{2}".format(self.randomWeightDict(self.poolName),self.randomWeightDict(self.poolName),random.randint(1,10000))
            rt[bType].append("TYPE="+nname)

            needList = ["",""]
            needList[1] = nname
            if isDebuff:
                needList[0] = "DAMAGE"
                rt[bType].append("NAME=DAMAGE OVER TIME")
                self.addToDesc("Damages over time ")
            else:
                needList[0] = "HEAL"
                rt[bType].append("NAME=HEAL OVER TIME")
                self.addToDesc("Heals over time ")
            self.needMove.append(needList)

        dAmt = random.randint(3,4)
        rt[bType].append("TARGET="+self.createTarget(mainTarget,isDebuff))   
        rt[bType].append("DUR="+str(dAmt))
        self.addToDesc("for {0} turns ".format(dAmt))

        rt[bType].append("COUNTTRI=SELFALLYENDTURN")
        rt[bType].append("ACT=EACHCOUNT")

        return rt
    
    def strSBuff(self,mainTarget,isDebuff,sc=1):
        bType = "BUFF"
        if (isDebuff):
            bType = "DEBUFF"

        amt = random.randint(15,50)*sc
        rt = {bType:[]}
        myDoList = {"STAT":1,"SLEEP":0.06,"STUN":0.1}
        for (k,v) in self.moveMech.items():
            if ("SLEEP" in k):
                myDoList["SLEEP"] = 1
            elif ("STUN" in k):
                 myDoList["STUN"] = 1

        myDo = self.randomWeightDict(myDoList)
        self.addToName(self.columns[myDo])
        if (myDo == "STAT"):
            
            namePrefix = "INCREASED_"
            baseCt = {"DAMAGE":1,"SPEED":1,"ARMOR":1,"DODGE":1,"ACCURACY":1,"CRIT":1} 
            if (isDebuff):
                bType = "DEBUFF"
                self.addToDesc("Debuffs ")
                amt *= -1
                namePrefix = "DECREASED_"
                baseCt["CRITCHANCERESIST"] = 1
                baseCt["CRITDAMAGERESIST"] = 1
            else:
                self.addToDesc("Buffs ")
                baseCt["CRITDAMAGE"] = 1
                baseCt["HEAL"] = 1
                baseCt["LIFESTEAL"] = 1
            rt[bType].append("DO=STAT")
            
            
            ct = self.randomWeightDict(baseCt)
        
            tStDict = self.statsPlus.copy()
            for (k,v) in self.moveMech.items():
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

            if ct in self.bonusMult0:
                amt *= self.bonusMult0[ct]

            rt[bType].append("TYPE="+ct)
            dAmt = random.randint(2,4)
            rt[bType].append("NAME="+namePrefix+ct)
            self.addToDesc("causing {0} ".format(namePrefix+ct))

            rt[bType].append("AMT="+str(amt))
            self.addToDesc("with amount {0} ".format(round(amt,1)))
            

        elif (myDo == "STUN" or myDo == "SLEEP"):
            dAmt = random.randint(1,3)
            rt[bType].append("NAME="+myDo)
            rt[bType].append("DO="+myDo)
            self.addToDesc("causing {0} ".format(myDo))

            self.addToName(self.columns["MECH"+myDo])

        rt[bType].append("TARGET="+self.createTarget(mainTarget,isDebuff))   
        rt[bType].append("DUR="+str(dAmt))
        self.addToDesc("for {0} turns ".format(dAmt))

        rt[bType].append("COUNTTRI=SELFALLYENDTURN")
        rt[bType].append("ACT=STARTCOUNT")

        return rt

    def strDamage(self,mainTarget,isHarm=True,sc=1):
        if (isHarm):
            tp = "DAMAGE"
            self.addToDesc("Deals damage ")
        else:
            tp = "HEAL"
            self.addToDesc("Heals damage ")
        rt = {tp:[]}
        dTypes = {"CRUSH":1,"PIERCE":1,"SLASH":1}
        
        if len(self.typePlus) > 0:
            # myType = self.randomWeightDict(self.typePlus)
            dTypes[self.randomWeightDict(self.typePlus)] = 4
        myType = self.randomWeightDict(dTypes)
        
        self.addToName(self.columns["TYPEPLUS"+myType])

        rt[tp].append("TYPE="+myType)
        self.addToDesc("for {0}*( ".format(round(sc,1)))
        dm = "{1}*({0})".format(self.createDamage(), sc)
        if (isHarm):
            rt[tp].append("AMT="+dm)
        else:
            rt[tp].append("AMT=-1*({0})".format(dm))

        
        self.addToDesc(") of type {0} ".format(myType))

        rt[tp].append("TARGET="+self.createTarget(mainTarget,isHarm))
        calcR = random.randint(0,15)
        calcB = random.randint(0,30)
        rt[tp].append("CRIT="+str(calcR))
        rt[tp].append("CRITBONUS="+str(calcB))
        return rt

    def strTrigger(self):
        acc = random.randint(75,110)
        t = ["HIT="+str(acc)]
        return t

    def strDo(self,mainTarget,sc=1):
        self.moveMech = {}
        for k,v in self.totalMech.items():
            nl = random.randint(1,10)/10
            self.moveMech[k] = nl

        for k,v in self.statsPlus.items():
            nl = random.randint(1,10)/10
            self.moveMech["STATPLUS{0}".format(k)] = nl

        rt = "DO="
        myDoChoices = {
                        "MECHDAMAGE":0.8,"MECHBUFFSTAT":0.3,
                        "MECHDEBUFFSTAT":0.4,"MECHHEAL":0.3,
                        "MECHOVERTIMEDAMAGE":0.44, "MECHOVERTIMEHEAL":0.2   
                        }
        for k in myDoChoices:
            if k in self.moveMech:
                myDoChoices[k]+=1

        myDo = self.randomWeightDict(myDoChoices)
        dc = {}
        if myDo == "MECHDAMAGE":
            dc = self.strDamage(mainTarget,True,sc=sc)
        elif myDo == "MECHBUFFSTAT":
            dc = self.strBuff(mainTarget,False,mtype="STAT",sc=sc)
        elif myDo == "MECHDEBUFFSTAT":
            dc = self.strBuff(mainTarget,True,mtype="STAT",sc=sc)
        elif myDo == "MECHHEAL":
            dc = self.strDamage(mainTarget,False,sc=sc)
        elif myDo == "MECHOVERTIMEDAMAGE":
            dc = self.strBuff(mainTarget,True,mtype="OVERTIME",sc=sc)
        elif myDo == "MECHOVERTIMEHEAL":
            dc = self.strBuff(mainTarget,False,mtype="OVERTIME",sc=sc)

        dc["TRIGGER"] = self.strTrigger()

        rt += json.dumps(dc)

        return rt

    def smallDo(self,myDo):
        rt = "DO="
        dc = {}
        if myDo == "DAMAGE":
            dc = self.strDamage("SELECTED",True,sc=0.4)
        elif myDo == "HEAL":
            dc = self.strDamage("SELECTED",False,sc=0.4)

        dc["TRIGGER"] = ["ALWAYS"]
        rt += json.dumps(dc)
        return rt

    def smallMove(self,needList):
        self.moveName = []
        self.moveDesc = []
        rt = "STARTMOVE\n"
        rt += "NAME={0}\n".format(needList[1])
        rt += self.smallDo(needList[0]) + "\n"
        self.moveLineDown()

        desc = ""
        for idx,x in enumerate(self.moveDesc):
            desc += x
            if idx != (len(self.moveDesc)-1):
                desc += "|"
        rt += "DESC={0}\n".format(desc)
        rt += "ENDMOVE\n"

        return rt

    def strMove(self):
        self.moveName = []
        self.moveDesc = []
        rt = "STARTMOVE\n"
        dos = []
        nl = random.randint(1,4)
        moveNumberWeights = {"1":1,"2":0.9,"3":0.5,"4":0.1,"5":0.05}
        moveNumberChoose = self.randomWeightDict(moveNumberWeights)
        mainTargetList = {"ALLY":0.3,"ENEMY":1}
        mainTarget = self.randomWeightDict(mainTargetList)

        numChoose = int(moveNumberChoose)
        for x in range(0,numChoose):
            dos.append(self.strDo(mainTarget,sc=1/numChoose))
            self.moveLineDown()

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

        desc = ""
        for idx,x in enumerate(self.moveDesc):
            desc += x
            if idx != (len(self.moveDesc)-1):
                desc += "|"
        rt += "DESC={0}\n".format(desc)

        rt += "ENDMOVE\n"


        
        return rt

    def totalChar(self):
        self.madeMoves = {}
        rt = ""
        moveNumberWeights = {"6":1}
        moveNumberChoose = self.randomWeightDict(moveNumberWeights)
        for x in range(int(moveNumberChoose)):
            rt += self.strMove()
        
        for x in self.needMove:
            rt += self.smallMove(x)
        self.needMove = []
            
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