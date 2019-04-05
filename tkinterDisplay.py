import tkinter as tk
import json
selectedFont = "Courier"
sizeFont = 20 

sizeFont2 = 15
sizeFont3 = 9

class displayClass:
    def __init__(self,g,m):
        self.ownerGame = g
        self.ownerGame.display = self
        self.messageLength = 10
        self.msgStart = 0
        self.messageList = []
        self.menu = m
        self.menu.display = self
        self.root = tk.Tk()
        #self.root.after(0, self.task)
        self.playerWindow = 0
        self.maxHeros = 4
        self.heroOffset = 0
        ####
        self.createMenu()
        self.root.mainloop()
        

    def rcd(self,msg):
        return msg.replace("_"," ")

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

    def resetMenu(self):
        self.menuFrame.destroy()
        self.createMenu()

    def createMenu(self):
        self.menuFrame = tk.Frame(self.root)
        self.menuFrame.grid()
        optionFrame = tk.Frame(self.menuFrame)
        optionFrame.grid(row=0,column=0)

        wikiFrame = tk.Frame(self.menuFrame)
        wikiFrame.grid(row=1,column=0)

        w0 = tk.Button(wikiFrame, font=(selectedFont,sizeFont),text="Obtain Wiki",command = lambda: self.windowWiki())
        w0.grid(row=0,column=0)

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

        for idx,x in enumerate(self.menu.queuePlayers):
            w0 = tk.Label(teamsContentFrame, font=(selectedFont,sizeFont),text="Team " + str(idx))
            w0.grid(row=0,column=idx)

            for idy, y in enumerate(x):
                w0 = tk.Button(teamsContentFrame, font=(selectedFont,sizeFont),text=self.rcd(y.getDisplayName()),command = lambda x0=x,y0=y: self.removePlayerFromTeam(x0,y0))
                w0.grid(row=idy+1,column=idx)

        ##############Player Options
        choosePlayerFrame = tk.Frame(playersFrame)
        choosePlayerFrame.grid(row = 0,column = 0,padx = 10, pady = 10)

        chooseScrollPlayerFrame = tk.Frame(choosePlayerFrame)
        chooseScrollPlayerFrame.grid(row = 0,column = 0,padx = 10, pady = 10)

        w0 = tk.Button(chooseScrollPlayerFrame, font=(selectedFont,sizeFont),text="^",command = lambda: self.scrollPlayer("C-1"))
        w0.grid(row=0,column=0)
        w0 = tk.Button(chooseScrollPlayerFrame, font=(selectedFont,sizeFont),text="v",command = lambda: self.scrollPlayer("C1"))
        w0.grid(row=1,column=0)

        optionPlayerFrame = tk.Frame(choosePlayerFrame)
        optionPlayerFrame.grid(row = 0,column = 1,padx = 10, pady = 10)

        playerLookStart = self.heroOffset
        playerLookEnd = min(len(self.menu.savedHeros),self.heroOffset + self.maxHeros)

        for idx in range(playerLookStart,playerLookEnd):
            cx = idx
            singleFrame = tk.Frame(optionPlayerFrame)
            singleFrame.grid(row=idx,column=0)
            nameButton = tk.Button(singleFrame, font=(selectedFont,sizeFont),text=self.rcd(self.menu.savedHeros[cx].getDisplayName()),command = lambda x0=self.menu.savedHeros[cx]: self.showSavedStats(x0))
            nameButton.grid(row=0,column=0)

            addTeamFrame = tk.Frame(singleFrame)
            addTeamFrame.grid(row=0,column=1)
            for y in range(self.menu.numTeams):
                addTeamButton = tk.Button(addTeamFrame, font=(selectedFont,sizeFont),text=self.rcd(str(y)),command = lambda x0=self.menu.savedHeros[cx],y0=y: self.addPlayerToTeam(x0,y0))
                addTeamButton.grid(row=0,column=y)

    def removePlayerFromTeam(self,team,y):
        team.remove(y)
        self.resetMenu()
        
    def addPlayerToTeam(self,player,team):
        self.menu.queuePlayers[team].append(player)
        self.resetMenu()

    def showSavedStats(self,player):
        print(player.getDisplayName())

    def startButton(self):
        if self.menu.startGameCheck():
            self.menuFrame.destroy()
            self.menu.addherosToGame()
            self.ownerGame.resetGame()
            
            self.createGui()
        

    def createGui(self):
        self.mainFrame = tk.Frame(self.root)
        self.mainFrame.grid()
        f0 = tk.Frame(self.mainFrame)
        f0.grid(row=0,column=1)
        w0 = tk.Button(f0, font=(selectedFont,sizeFont),text="End Turn",command = lambda: self.endTurn())
        w0.grid(row=0,column=0)

        self.allPlayers = tk.Frame(f0)
        self.allPlayers.grid(column = 0, row = 1)

        self.playerFrames = []
        for x in range(len(self.ownerGame.players)):
            pf = tk.Frame(self.allPlayers)
            pf.grid(row=x)
            self.playerFrames.append(pf)

        self.fillTeams()
        messageFrame = tk.Frame(self.mainFrame)
        messageFrame.grid(row=0,column=0)
        messageText = tk.Frame(messageFrame)
        messageText.grid(row=0,column=0)
        ###
        messageButtonFrame = tk.Frame(messageFrame)
        messageButtonFrame.grid(row=0,column=1)

        w0 = tk.Button(messageButtonFrame, font=(selectedFont,sizeFont),text="^",command = lambda: self.scrollMessage("C1"))
        w0.grid(row=0,column=0)
        w0 = tk.Button(messageButtonFrame, font=(selectedFont,sizeFont),text="v",command = lambda: self.scrollMessage("C-1"))
        w0.grid(row=1,column=0)

        self.fillMessage(messageText)


    def scrollPlayer(self,act):
        if act == "C1":
            self.heroOffset += self.maxHeros
        elif act == "C-1":
            self.heroOffset -= self.maxHeros
        if self.heroOffset < 0:
            self.heroOffset = 0
            
        mx = max(len(self.menu.savedHeros)-self.maxHeros,0)

        if self.heroOffset > mx:
            self.heroOffset = mx
        self.resetMenu()

    def scrollMessage(self,act):
        if act == "C1":
            self.msgStart +=1
        elif act == "C-1":
            self.msgStart -= 1
        if self.msgStart < 0:
            self.msgStart = 0
        mx = max(len(self.ownerGame.visibleMessage)-self.messageLength,0)
        if self.msgStart > mx:
            self.msgStart = mx
        self.updateMessageFrame()


    def updateMessageFrame(self):
        for idx,x in enumerate(reversed(self.messageList)):
            if len(self.ownerGame.visibleMessage) > idx:
                msgLook = len(self.ownerGame.visibleMessage)-1-idx-self.msgStart
                t = self.ownerGame.visibleMessage[msgLook]
                x.config(text=self.rcd(str(t)))

    def takeGameMessage(self,msg):
        self.updateMessageFrame()

    def fillMessage(self,f):
        self.messageList = []
        for x in range(self.messageLength):
            
            w0 = tk.Label(f, font=(selectedFont,sizeFont2),text="")
            w0.grid(row=x,column=0,rowspan=1,sticky="s")
            self.messageList.append(w0)
        self.takeGameMessage("TEXT")

    def fillTeams(self):
        teams = self.ownerGame.getTeams()    
        for idx,x in enumerate(teams):
            self.fillPlayers(self.playerFrames[idx],x,idx)

    def fillPlayers(self,f,team,teamNum):     
        for idx,x in enumerate(team):
            w0 = tk.Button(self.allPlayers, font=(selectedFont,sizeFont),text=self.rcd(x.getDisplayName()),command = lambda x0=x: self.windowPlayer(x0))
            w0.grid(row=teamNum,column=idx)
            if x.myTurn:
                w0.config(bg="blue")

    def fillTeamsTarget(self,player,skill,window):
        teams = self.ownerGame.getTeams()    
        for idx,x in enumerate(teams):
            self.fillPlayersTarget(x,idx,window,player,skill)

    def fillPlayersTarget(self,team,teamNum,window,player,skill):     
        for idx,x in enumerate(team):
            w0 = tk.Button(window, font=(selectedFont,sizeFont),text=self.rcd(x.getDisplayName()),command = lambda p0=player,x0=x,s0=skill: self.playerUseSkill(p0,x0,s0))
            w0.grid(row=teamNum,column=idx)
            if x == player:
                w0.config(bg="blue")
            elif x.team == player.team:
                w0.config(bg="green")
            else:
                w0.config(bg="red")
            

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
        w0 = tk.Label(newWin, font=(selectedFont,sizeFont),text=self.rcd(player.getDisplayName()))
        w0.grid(row=0)
        w0 = tk.Label(newWin, font=(selectedFont,sizeFont),text=self.rcd(skillName))
        w0.grid(row=1)
        w0 = tk.Label(newWin, font=(selectedFont,sizeFont),text=self.rcd(player.getMoveByName(skillName).desc))
        w0.grid(row=2)

        
        targetFrame = tk.Frame(newWin)
        targetFrame.grid(row=3)
        self.fillTeamsTarget(player,skillName,targetFrame)

    def windowBuffs(self,player):
        statsRow = 2
        newWin = tk.Toplevel(self.root)
        newWin.grid()
        #####
        w0 = tk.Label(newWin, font=(selectedFont,sizeFont2),text="BUFFS") 
        w0.grid(row=0)
        s0Frame = tk.Frame(newWin)
        s0Frame.grid(row=1)
        cc = 0
        rc = 0
        for idx, (key) in enumerate(player.buffs):     
            tx = "{0}: {1} ".format(self.rcd(key.name),key.value)
            w0 = tk.Label(s0Frame, font=(selectedFont,sizeFont2),text=tx)    
            w0.grid(column=cc,row=rc)
            cc += 1
            if (cc > statsRow):
                cc = 0
                rc += 1

    def windowStats(self,player):
        statsRow = 5
        newWin = tk.Toplevel(self.root)
        newWin.grid()
        ################################
        w0 = tk.Label(newWin, font=(selectedFont,sizeFont2),text="STATS") 
        w0.grid(row=0)
        s0Frame = tk.Frame(newWin)
        s0Frame.grid(row=1)
        cc = 0
        rc = 0
        for idx, (key, value) in enumerate(player.stats.items()):     
            tx = "{0}: {1} ".format(key,value)
            w0 = tk.Label(s0Frame, font=(selectedFont,sizeFont2),text=tx)    
            w0.grid(column=cc,row=rc)
            cc += 1
            if (cc > statsRow):
                cc = 0
                rc += 1
        ################################
        w0 = tk.Label(newWin, font=(selectedFont,sizeFont2),text="Resist") 
        w0.grid(row=2)
        s0Frame = tk.Frame(newWin)
        s0Frame.grid(row=3)
        cc = 0
        rc = 0
        for idx, (key, value) in enumerate(player.typeResist.items()):   
            if (value != 0):
                tx = "{0}: {1} ".format(key,value)
                w0 = tk.Label(s0Frame, font=(selectedFont,sizeFont2),text=tx)    
                w0.grid(column=cc,row=rc)
                cc += 1
                if (cc > statsRow):
                    cc = 0
                    rc += 1
        ################################
        w0 = tk.Label(newWin, font=(selectedFont,sizeFont2),text="Damage") 
        w0.grid(row=4)
        s0Frame = tk.Frame(newWin)
        s0Frame.grid(row=5)
        cc = 0
        rc = 0
        for idx, (key, value) in enumerate(player.typeDamage.items()):   
            if (value != 0):  
                tx = "{0}: {1} ".format(key,value)
                w0 = tk.Label(s0Frame, font=(selectedFont,sizeFont2),text=tx)    
                w0.grid(column=cc,row=rc)
                cc += 1
                if (cc > statsRow):
                    cc = 0
                    rc += 1
        ################################
        w0 = tk.Label(newWin, font=(selectedFont,sizeFont2),text="Types") 
        w0.grid(row=6)
        s0Frame = tk.Frame(newWin)
        s0Frame.grid(row=7)
        cc = 0
        rc = 0
        for idx, value in enumerate(player.typeRace):   
            tx = "{0}".format(value)
            w0 = tk.Label(s0Frame, font=(selectedFont,sizeFont2),text=tx)    
            w0.grid(column=cc,row=rc)
            cc += 1
            if (cc > statsRow):
                cc = 0
                rc += 1

    def loadArticle(self,t):
        tinput = t.get("1.0",tk.END)
        tinput = tinput.rstrip()
        #print(tinput)
        self.menu.loadArticle(tinput)
        
        self.menu.loadHerosFromFiles()
        self.resetMenu()
        self.resetWiki()

    def loadHero(self):
        self.menu.genHero()
        self.resetWiki()

    def resetWiki(self):
        self.wikiFrame.destroy()
        self.windowWiki()

    def windowArticle(self,a):
        newWin = tk.Toplevel(self.root)
        newWin.grid()
        t = tk.Label(newWin, text=a.name,font=(selectedFont,sizeFont))
        t.grid(column=0,row=0)


        tx0 = sorted(a.t2, key=a.t2.get, reverse=True)[:self.menu.numWords] 
        tx1 = ""
        for k in tx0:
            tx1 += "{0} ".format(k)

        t = tk.Message(newWin,text=tx1, font=(selectedFont,sizeFont2))
        t.grid(column=0,row=1)


    def windowWiki(self):
        newWin = tk.Toplevel(self.root)
        newWin.grid()
        self.wikiFrame = newWin
        wkFrame = tk.Frame(newWin)
        wkFrame.grid(row=0,column=0)
        t = tk.Text(wkFrame, height=1, width=30,font=(selectedFont,sizeFont))
        t.grid(column=0,row=0)
        w0 = tk.Button(wkFrame, font=(selectedFont,sizeFont),text="Load Article",command = lambda t=t :self.loadArticle(t))    
        w0.grid(column=0,row=1)
        w0 = tk.Button(wkFrame, font=(selectedFont,sizeFont),text="Make Character",command = lambda :self.loadHero())    
        w0.grid(column=0,row=2)

        w0 = tk.Label(wkFrame, font=(selectedFont,sizeFont),text="Loaded Articles:")
        w0.grid(row=3)
        loadFrame = tk.Frame(newWin)
        loadFrame.grid(row=4,column=0)
        for idx,x in enumerate(self.menu.loadWiki):
            eFrame = tk.Frame(loadFrame)
            eFrame.grid(column=0,row=idx)
            w0 = tk.Label(eFrame, font=(selectedFont,sizeFont),text=x.name)
            w0.grid(column=0,row=0)

            w0 = tk.Button(eFrame, font=(selectedFont,sizeFont),text="Scores",command = lambda x=x : self.windowArticle(x))    
            w0.grid(column=1,row=0)

        w0 = tk.Label(newWin, font=(selectedFont,sizeFont),text="Matched KeyWords:")
        w0.grid(row=5)
        #tx = json.dumps(self.menu.matched)
        #print(self.menu.matched)
        tx = self.menu.matched
        #for k,v in self.menu.matched.items():
        #    tx += "{0}-{1},".format(k,v)
        t = tk.Message(newWin,text=tx, font=(selectedFont,sizeFont3))
        t.grid(column=0,row=6)


        

    def warnFewKeyWord(self,match,less,suggList):
        newWin = tk.Toplevel(self.root)
        newWin.grid()
        w0 = tk.Label(newWin, font=(selectedFont,sizeFont),text="Found {0} of {1}keywords, suggested articles:".format(match,less))
        w0.grid(row=0)
        other = ""
        for x in suggList:
            other += x + ", "

        w0 = tk.Text(newWin,height=5, width=30, font=(selectedFont,sizeFont),text=other.format(less))
        w0.grid(row=1)

    def windowPlayer(self,player):
        newWin = tk.Toplevel(self.root)
        newWin.grid()
        self.playerWindow = newWin
        w0 = tk.Label(newWin, font=(selectedFont,sizeFont),text=player.getDisplayName())
        w0.grid(row=0)

        w0 = tk.Label(newWin, font=(selectedFont,sizeFont),text=player.textHealth())
        w0.grid(row=1)

        sFrame = tk.Frame(newWin)
        sFrame.grid(column=0,row=2)

        w0 = tk.Button(sFrame, font=(selectedFont,sizeFont),text="Stats",command = lambda p=player : self.windowStats(p))    
        w0.grid(column=0,row=0)

        w0 = tk.Button(sFrame, font=(selectedFont,sizeFont),text="Buffs",command = lambda p=player : self.windowBuffs(p))    
        w0.grid(column=1,row=0)

        moveFrame = tk.Frame(newWin)
        moveFrame.grid(row=3)

        movesPerRow = 4
        cc = 0
        rc = 0

        for idx,x in enumerate(player.moveList()):
            

            skillName = x.name
            w0 = tk.Button(moveFrame, font=(selectedFont,sizeFont),text=self.rcd(skillName),command = lambda p=player,y=skillName : self.windowTarget(p,y))    
            w0.grid(column=cc,row=rc)
            cc += 1
            if cc >= movesPerRow:
                cc = 0
                rc += 1