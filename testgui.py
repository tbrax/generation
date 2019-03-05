from tkinterDisplay import *
from game import *
from menu import *

def main():

    g = Game()
    m = Menu(g)
    d = displayClass(g,m)

if __name__== "__main__":
    main()
