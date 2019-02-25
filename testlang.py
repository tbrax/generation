import wikipedia
import os
import re
import heapq
#from nltk.stem.lancaster import LancasterStemmer
#class Keyget:

    #def __init__(self):


folderName = "articles"
stopLoc = "keywords\\stopwords.txt"

def cleanText(text):
    rtext = text
    rtext = re.sub(r'\W+ ', ' ', rtext)
    return rtext.lower()


def loadWiki(fname):
    found = 0
    for filename in os.listdir(folderName):
        if filename == (fname+".txt"):
            print("Document already exists")
            found = 1
    if found == 0:
        try:
            wka = wikipedia.page(fname)
            encodedStr = wka.content
            with open("articles\\"+fname + ".txt", "w", encoding="utf-8") as f:
                f.write(encodedStr)
            with open("links\\"+fname + ".txt", "w", encoding="utf-8") as f:
                for x in wka.links:
                    addS = str(x) + " "
                    f.write(addS)
            with open("summary\\"+fname + ".txt", "w", encoding="utf-8") as f:
                f.write(wka.summary)

        except wikipedia.exceptions.DisambiguationError as e:
            print(e.options)


def loadFile(name):
    with open(name,encoding="utf8") as myfile:
        return myfile.read().replace('\n', ' ')

def loadText(text):
    return loadFile(folderName+"\\"+text+".txt")

def computeTF(textList):
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

def computeIDF(textList):
    stops = loadFile(stopLoc).lower()
    stops = stops.split()
    for x in stops:
        if x in textList:
            textList[x] = 0.0
    return textList


def computeText(text):
    loadWiki(text)
    t0 = loadText(text)
    t0 = cleanText(t0)
    t1 = t0.split()
    t2 = computeTF(t1)

    t2 = computeIDF(t2)

    t3 = heapq.nlargest(5, t2, key=t2.get)
    print(t3)



def main():
    computeText("computer")
    
if __name__== "__main__":
    main()
