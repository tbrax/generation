import tkinter as tk
selectedFont = "Courier"
sizeFont = 20 

class displayClass:
    def __init__(self,g,m):
        self.ownerGame = g
        self.menu = m
        self.root = tk.Tk()
        #self.root.after(0, self.task)
        self.playerWindow = 0
        self.createMenu()
        self.root.mainloop()


    def task(self):
        self.root.after(1000, self.task)

    def resetGui(self):
        self.mainFrame.destroy()
        self.createGui()

    def endTurn(self):
        self.ownerGame.endTurn()
        #for x in self.ownerGame.turnOrder:
        #    print(x.getDisplayName())
        #print(self.ownerGame.turnOrder[self.ownerGame.turnCurrent].getDisplayName() + "'s Turn")
        self.resetGui()

    def createMenu(self):
        self.menuFrame = tk.Frame(self.root)
        self.menuFrame.grid()
        optionFrame = tk.Frame(self.menuFrame)
        optionFrame.grid(row=0,column=0)

        w0 = tk.Button(optionFrame, font=(selectedFont,sizeFont),text="Start Game",command = lambda: self.startButton())
        w0.grid(row=0,column=0)

        playersFrame = tk.Frame(optionFrame)
        playersFrame.grid(row=1,column=0)
        ################ Teams
        teamsFrame = tk.Frame(playersFrame)
        teamsFrame.grid(row=0,column=1)
        teamsTitleFrame = tk.Frame(teamsFrame)
        teamsTitleFrame.grid(row=0,column=0)
        teamsContentFrame = tk.Frame(teamsFrame)
        teamsContentFrame.grid(row=1,column=0)
        for x in range(self.menu.numTeams):
            w0 = tk.Button(teamsTitleFrame, font=(selectedFont,sizeFont),text="Team " + str(x),command = lambda: self.startButton())
            w0.grid(row=0,column=0)
        ##############Player Options
        optionPlayerFrame = tk.Frame(playersFrame)
        optionPlayerFrame.grid(row = 0,column = 1)
        for idx,x in enumerate(self.menu.savedHeroes):
            singleFrame = tk.Frame(optionPlayerFrame)
            singleFrame.grid(row=idx,column=0)
            nameButton = tk.Button(singleFrame, font=(selectedFont,sizeFont),text=x.getDisplayName(),command = lambda x0=x: self.showSavedStats(x0))
            nameButton.grid(row=0,column=0)

            addTeamFrame = tk.Frame(singleFrame)
            addTeamFrame.grid(row=0,column=1)
            for y in range(self.menu.numTeams):
                addTeamButton = tk.Button(addTeamFrame, font=(selectedFont,sizeFont),text=str(y),command = lambda x0=x,y0=y: self.addPlayerToTeam(x0,y0))
                addTeamButton.grid(row=0,column=y)

    def addPlayerToTeam(self,player,team):
        print("Add not implemented")

    def showSavedStats(self,player):
        print(player.getDisplayName())
    def startButton(self):
        self.menuFrame.destroy()
        self.ownerGame.resetGame()
        self.menu.addHeroesToGame()
        self.createGui()
        

    def createGui(self):
        self.mainFrame = tk.Frame(self.root)
        self.mainFrame.grid()

        w0 = tk.Button(self.mainFrame, font=(selectedFont,sizeFont),text="End Turn",command = lambda: self.endTurn())
        w0.grid(row=0,column=0)

        self.allPlayers = tk.Frame(self.mainFrame)
        self.allPlayers.grid(column = 0, row = 1)

        self.playerFrames = []
        for x in range(len(self.ownerGame.players)):
            pf = tk.Frame(self.allPlayers)
            pf.grid(row=x)
            self.playerFrames.append(pf)

        self.fillTeams()

    def fillTeams(self):
        teams = self.ownerGame.getTeams()    
        for idx,x in enumerate(teams):
            self.fillPlayers(self.playerFrames[idx],x,idx)

    def fillPlayers(self,f,team,teamNum):     
        for idx,x in enumerate(team):
            w0 = tk.Button(self.allPlayers, font=(selectedFont,sizeFont),text=x.getDisplayName(),command = lambda x0=x: self.windowPlayer(x0))
            w0.grid(row=teamNum,column=idx)

    def fillTeamsTarget(self,player,skill,window):
        teams = self.ownerGame.getTeams()    
        for idx,x in enumerate(teams):
            self.fillPlayersTarget(x,idx,window,player,skill)

    def fillPlayersTarget(self,team,teamNum,window,player,skill):     
        for idx,x in enumerate(team):
            w0 = tk.Button(window, font=(selectedFont,sizeFont),text=x.getDisplayName(),command = lambda p0=player,x0=x,s0=skill: self.playerUseSkill(p0,x0,s0))
            w0.grid(row=teamNum,column=idx)

    def playerUseSkill(self,player,target,skill):
        #print(player.getDisplayName())
        #print(target.getDisplayName())
        player.useMove(skill,target)
        self.resetPlayerWindow(player)
        self.closeTargetWindow()

    def resetPlayerWindow(self,player):
        self.playerWindow.destroy()
        self.playerWindow = 0
        self.windowPlayer(player)

    def closePlayerWindow(self):
        self.playerWindow.destroy()
        self.playerWindow = 0

    def closeTargetWindow(self):
        self.targetWindow.destroy()
        self.targetWindow = 0

    def windowTarget(self,player,skillName):
        newWin = tk.Toplevel(self.root)
        newWin.grid()
        self.targetWindow = newWin
        w0 = tk.Label(newWin, font=(selectedFont,sizeFont),text=player.getDisplayName())
        w0.grid(row=0)
        w0 = tk.Label(newWin, font=(selectedFont,sizeFont),text=skillName)
        w0.grid(row=1)
        targetFrame = tk.Frame(newWin)
        targetFrame.grid(row=2)
        self.fillTeamsTarget(player,skillName,targetFrame)

    def windowPlayer(self,player):
        newWin = tk.Toplevel(self.root)
        newWin.grid()
        self.playerWindow = newWin
        w0 = tk.Label(newWin, font=(selectedFont,sizeFont),text=player.getDisplayName())
        w0.grid(row=0)

        w0 = tk.Label(newWin, font=(selectedFont,sizeFont),text=player.textHealth())
        w0.grid(row=1)

        moveFrame = tk.Frame(newWin)
        moveFrame.grid(row=2)
        for idx,x in enumerate(player.moveList()):
            skillName = x.name
            w0 = tk.Button(moveFrame, font=(selectedFont,sizeFont),text=skillName,command = lambda p=player,y=skillName : self.windowTarget(p,y))    
            w0.grid(row=idx)