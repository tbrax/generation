
class MoveOrder:
    def __init__(self):
        self.am = "DAMAGE"
        self.type = "CRUSH"
        self.triggers = []
        self.heldValue = 0
        self.tar = "SELECTED"


    def activate(self,user,target):
        totalTargets = []
        if self.am == "DAMAGE":
            user.dealDamage(target,self.heldValue,self.type)

    def load(self,data):
        for key, value in data.items():
            if key == "DAMAGE":
                self.am = "DAMAGE"
                for x in value:
                    if x.startswith("AMT="):
                        self.heldValue = float(x[4:])
                    elif x.startswith("TYPE="):
                        self.type = x[5:]
                    elif x.startswith("TARGET="):
                        self.tar = x[7:]