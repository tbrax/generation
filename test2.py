
import wikipedia
from textblob import TextBlob as tb
from textgenrnn import textgenrnn
import math
import os

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)
            

def loadFromFile(f):
    file = open(f, "r") 
    fileStr=file.read().replace('\n', '')
    return fileStr

def loadFromFolder(folderName):
    bloblist = []
    for filename in os.listdir(folderName):
        with open(folderName+"\\"+filename,encoding="utf8") as myfile:
            readFile=myfile.read().replace('\n', '')
            bloblist.append(tb(readFile.lower()))
    return bloblist

def main():
    fname = "Mushroom"
    dirName = "articles"
    option = 3
    if option == 3:
        textgen = textgenrnn()
        ts = loadFromFolder(dirName)
        textgen.train_on_texts(ts,num_epochs=1)
        gens = textgen.generate(5,return_as_list = True)
        
    elif option == 2:
        for filename in os.listdir("articles"):
            try:
                artFile = loadFromFile("articles\\" + filename)
            except:
                print("Error loading file " + filename)

    elif option == 0:
        bloblist = []
        for filename in os.listdir("articles"):
            with open("articles\\"+filename,encoding="utf8") as myfile:
                readFile=myfile.read().replace('\n', '')
                bloblist.append(tb(readFile.lower()))

        
        for i, blob in enumerate(bloblist):
            print("Top words in document {}".format(i + 1))
            scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
            sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            for word, score in sorted_words[:3]:
                print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))

    elif (option == 1):
        found = 0
        for filename in os.listdir("articles"):
            if filename == fname:
                print("Document already exists")
                found = 1
        if found == 0:
            try:
                wka = wikipedia.page(fname)
                encodedStr = wka.content
                with open("articles\\"+fname + ".txt", "w", encoding="utf-8") as f:
                    f.write(encodedStr)

            except wikipedia.exceptions.DisambiguationError as e:
                print(e.options)



if __name__== "__main__":
    main()
