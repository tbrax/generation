import wikipedia
import os
import re
import heapq
import nltk
from nltk.corpus import wordnet

class tf:
    def __init__(self):
        self.folderName = "articles"
        self.stopLoc = "keywords\\stopwords.txt"
        self.linksName = "links"
        self.t2 = {}
        self.links = []
        self.name = ""
        self.loaded = "NONE"
        self.options = []

    def cleanText(self,text):
        rtext = text
        rtext = re.sub(r'\W+ ', ' ', rtext)
        return rtext.lower()


    def loadWiki(self,fname):
        found = 0
        for filename in os.listdir(self.folderName):
            if filename == (fname+".txt"):
                #print("Document already exists")
                found = 1
                self.loaded = "LOADED"
                return True
        if found == 0:
            try:
                wka = wikipedia.page(fname)
                encodedStr = wka.content
                with open("articles\\"+fname + ".txt", "w", encoding="utf-8") as f:
                    f.write(encodedStr)
                with open("links\\"+fname + ".txt", "w", encoding="utf-8") as f:
                    for x in wka.links:
                        addS = str(x) + "|"
                        f.write(addS)
                with open("summary\\"+fname + ".txt", "w", encoding="utf-8") as f:
                    f.write(wka.summary)
                self.loaded = "LOADED"
                return True

            except wikipedia.exceptions.DisambiguationError as e:
                #print(e.options)
                self.options = e.options
                self.loaded = "DISAMBIG"
                return False


    def loadFile(self,name):
        with open(name,encoding="utf8") as myfile:
            return myfile.read().replace('\n', ' ')

    def loadText(self,text):
        return self.loadFile(self.folderName+"\\"+text+".txt")

    def computeTF(self,textList):
        dictTF = {}

        for x in textList:

            if x not in dictTF:
                dictTF[x] = 1.0
            else:
                dictTF[x] += 1.0
        for word,value in dictTF.items(): 
            value = float(value) / float(len(textList))
            dictTF[word] = value
        return dictTF

    def computeIDF(self,textList):
        stops = self.loadFile(self.stopLoc).lower()
        stops = stops.split()
        for x in stops:
            if x in textList:
                textList[x] = 0.0
        return textList

    def getLinks(self,topList):
        text = self.name
        f = self.loadFile(self.linksName+"\\"+str(text)+".txt").lower()
        fList = f.split("|")
        links = []
        for x in topList:
            if x.lower() in fList:
                links.append(x)
        return links
    def addSyn(self,ls):
        syn = {}
        for (k,v) in ls.items():
            for synset in wordnet.synsets(k):
                for lemma in synset.lemmas():
                    syn[lemma.name()] = v    #add the synonyms
        return syn

    def computeText(self,text):
        
        if (self.loadWiki(text)):
            self.name = text
            t0 = self.loadText(text)
            t0 = self.cleanText(t0)
            t1 = t0.split()
            t2 = self.computeTF(t1)

            t2 = self.computeIDF(t2)
            #links = self.getLinks(text,t3)
            #self.links = links

            self.t2 = t2
            #print(t2)
            
            #print(t3)
            #print(links)
            #print('Synonyms: ' + str(syn))
    
