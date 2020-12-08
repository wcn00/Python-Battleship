from board import board
from player import player
import os,sys
import time

if __name__ == '__main__':
    autoPlay = False
    display = False
    for arg in sys.argv[1:]:
        if arg == '-a':
            autoPlay = True
        elif arg == '-ui':
            display = True
    playerA = player("Kane",autoPlay) 
    playerB = player("Able",autoPlay) 

    if autoPlay:
        while True:
            if playerA.go(playerB.board):
                print(playerA.playername + " has won!!!")
                break
            if playerB.go(playerA.board):
                print(playerB.playername + " has won!!!")
                break
            time.sleep(.2)
    print("\nGame Over\n")