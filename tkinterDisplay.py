import tkinter as tk
selectedFont = "Courier"
sizeFont = 20 

class displayClass:
    def __init__(self,g):
        self.ownerGame = g
        self.root = tk.Tk()
        #self.root.after(0, self.task)
        self.createGui()
        self.root.mainloop()


    def task(self):
        self.root.after(1000, self.task)

    def createGui(self):
        self.mainFrame = tk.Frame(self.root)
        self.mainFrame.grid()
        self.allPlayers = tk.Frame(self.mainFrame)

        numPlayers = 2
        self.playerFrames = []
        for x in range(numPlayers):
            pf = tk.Frame(self.allPlayers)
            pf.grid(row=x)
            self.playerFrames.append(pf)

        self.fillTeams()

    def fillTeams(self):
        teams = self.ownerGame.getTeams()
        
        for idx,x in enumerate(teams):
            self.fillPlayers(self.playerFrames[idx],x)

    def fillPlayers(self,f,team):
        
        for idx,x in enumerate(team):
            w0 = tk.Button(self.mainFrame, font=(selectedFont,sizeFont),text=x.getDisplayName(),command = lambda: self.windowPlayer(x))
            w0.grid(row=0,column=idx)

    def playerUseSkill(self,player,skill):
        player.useMove(skill,player)

    def windowPlayer(self,player):
        newWin = tk.Toplevel(self.root)
        newWin.grid()

        w0 = tk.Label(newWin, font=(selectedFont,sizeFont),text=player.getDisplayName())
        w0.grid(row=0)

        moveFrame = tk.Frame(newWin)
        moveFrame.grid(row=1)
        for idx,x in enumerate(player.moveList()):
            skillName = x.name
            w0 = tk.Button(moveFrame, font=(selectedFont,sizeFont),text=skillName,command = lambda p=player,y=skillName : self.playerUseSkill(p,y))    
            w0.grid(row=idx)




    def showGame(self,game):
         print("Wow")