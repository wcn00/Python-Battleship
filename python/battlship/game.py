from board import board
from player import player
from display import display
import os
import sys
import time

def usage():
    print("Usage:  python game.py <option>")
    print("options:")
    print("--quiet           do not bombing and sooting sounds")
    print("--manual          allow player A to choose their own bombing sites")
    print("--curses-display  display the boards via curses")


if __name__ == '__main__':
    """This is the setup and main loop for the game"""
    autoPlay = True
    quiet = False
    playerA = None
    playerB = None
    curses_display = False
    for arg in sys.argv[1:]:
        if arg == '--quiet':
            quiet = True
        elif arg == '--manual':
            autoPlay = False
        elif arg == '--curses-display':
            curses_display = True
        elif arg == '-h' or arg == '--help':
            usage()
    curses_display = display(curses_display)
    playerA = player("Kane", curses_display,quiet,autoPlay,leftPlayer = True)
    playerB = player("Able", curses_display,quiet,True,leftPlayer = False)
    while True:
        playerA.print_board()
        playerB.print_board()

        if playerA.go(playerB.board):
            playerA.print_board()
            playerB.print_board()
            playerB.player_print("you sank my battleship!")
            break
        if playerB.go(playerA.board):
            playerA.print_board()
            playerB.print_board()
            playerA.player_print("you sank my battleship!")
            break
    playerA.resetdisplay()
