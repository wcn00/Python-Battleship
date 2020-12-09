from board import board
from player import player
import os,sys
import time

def getOrientationHorizontal():
    while True:
        orientation = input("Enter 'H' for Horizontal or 'V' for virticle ship orientation: ")
        if len(orientation) >0 and orientation.lower()[0] == 'h':
            return True
            break
        elif len(orientation) >0 and orientation.lower()[0] == 'v':
            return False
            break
    

if __name__ == '__main__':
    autoPlay = True
    display = False
    quiet = False
    playerA = None
    PlayerB = None
    for arg in sys.argv[1:]:
        if arg == '--quiet':
            quiet = True
        elif arg == '--manual':
            autoPlay = False
    
    if autoPlay:
        playerA = player("Kane",autoPlay)
    else :
        playerAName = input("Please enter your name: ")
        playerA = player(playerAName,autoPlay,quiet)
        shipCell = playerA.getCellToBombFromPlayer(playerA.board,"Enter the midship cell for your ship: ","")
        playerA.board.allocShip(getOrientationHorizontal(),shipCell)

    playerB = player("Able",True,quiet)

    while True:
        if playerA.go(playerB.board):
            print(playerB.playername + ": you sank my battleship!")
            break
        if playerB.go(playerA.board):
            print(playerA.playername + ": you sank my battleship!")
            break
        time.sleep(.2)
    print("\nGame Over\n")