from hero import Hero
from move import Move

class Game:
    def __init__(self):
        self.players = []
        self.selected = 0
        self.target = 0
        #self.messageDest = 0
        self.messageQueue = []

    def makePlayer(self,name):
        p = Hero()
        p.ownerGame = self
        p.name = name
        p.addMove("Punch")
        self.players.append(p)

    def checkPlayer(self,owner):
        found = 0
        for x in self.players:
            if x.name == owner:
                found = 1
        if found == 0:
            self.makePlayer(owner)

    def cmdMe(self,owner):
        self.checkPlayer(owner)
        send = []
        
        for x in self.players:
            if x.name == owner:
                send += x.info()

        self.addMessage(send)

    def addMessage(self,msg):
       
        self.messageQueue += msg

    def help(self):
        send = []
        send += {"Commands:"}
        send += {"!me - lists your character's stats"}
        send += {"!fight - looks for a fight"}

        send += {"!move - Lists all your moves. Give it a move to tell you about it. Ex: !move shotgun or !move 0"}
        send += {"!use - Uses a specified move. Ex: !use shotgun or !use 0"}
        send += {"!inv - Displays your character's inventory"}
        send += {"!status - Shows buffs and debuffs on your character"}
        send += {"!die - You die"}

        self.addMessage(send)

    def useMove(self,move,owner):
        self.checkPlayer(owner)
        trueMove = move.replace("!USE ","")
        if trueMove == "":
            for x in self.players:
                if x.name == owner:
                    x.listMoves()
        else:
            for x in self.players:
                if x.name.upper() == owner.upper():
                    x.useMove(trueMove,x)


    def loadMove(self,name):
        
        newMove = Move()
        newMove.name = name.upper()

        newMove.createMove()
        if newMove.loaded != 2:
            return 0
        return newMove

    def explainMove(self,name):
        trueName = name.replace("!MOVE ","")

        trueName = trueName.upper()
        newMove = self.loadMove(trueName)
        if newMove == 0:
            self.addMessage("The move {0} does not exist".format(trueName))
        else:
            self.addMessage(newMove.describe())

    def takeInput(self,textInput,owner):
        t = textInput.upper()
        self.messageQueue = []
        if t == "!ME":
            self.cmdMe(owner)
        elif t == "!HELP":
            self.help()

        elif t.startswith("!USE"):
            self.useMove(t,owner)

        elif t.startswith("!MOVE"):
            self.explainMove(t)

        return self.messageQueue

    def tryMove(self):
        print("Mv")
