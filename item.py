class Item:
    def __init__(self,owner):
        self.owner = owner
        self.amt = 1
        #0 consumable 1 stat
        self.type = 0
        self.useMove = ""

    def reduceAmt(self):
        self.amt -= 1

    def checkUse(self):
        if self.amt > 0:
            return True
        return False

    def use(self):
        if self.checkUse():
            self.reduceAmt()
            self.owner.activateMove(self.use,self.owner)
        
 