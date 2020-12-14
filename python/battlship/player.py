from board import board,cell
from display import display
import random
import time

class player:
    def __init__(self,name:str,curses_display:display, silent=False,autoPlay=True,leftPlayer=True):
        horizontal = random.randint(0, 100) % 2 == 1
        self.playername = name
        self.leftPlayer = leftPlayer
        self.auto = autoPlay
        self.opponentShip = []
        self.hitState = 0
        self.attackNext = []
        self.curses_display = curses_display
        self.shipcell=None
        if not self.auto:
            self.playername = self.curses_display.req_reply("Please enter your name: ")
            orientation = self.curses_display.req_reply("Enter 'H' for Horizontal or 'V' for virticle ship orientation: ")
            self.horizontal = len(orientation) > 0 and orientation.lower()[0] == 'h'
            self.board = board(self.playername, silent)
            while True:
                shipcellspec = self.curses_display.req_reply("Please enter the cell on which to place your ship: ")
                if len(shipcellspec)>=2 and shipcellspec[0] in board.rownames and shipcellspec[1].lower() in board.colnames:
                    self.shipCell = self.board.allocShipByCoorid(horizontal,shipcellspec[0],shipcellspec[1].lower())
                    break;
            self.curses_display.settitle(self.playername,self.leftPlayer)
        else:
            self.board = board(self.playername, silent)
            self.ship = self.board.allocRandomShip(horizontal)
            self.curses_display.settitle(self.playername,self.leftPlayer)

    def printboard(self):
        self.curses_display.printBoard(self.playername,self.board,self.leftPlayer)
        
    def printMsg(self,msg:str):
        self.curses_display.print_status(msg)

    def playerPrint(self,msg:str):
        self.curses_display.print_status(self.playername+": "+msg)
        
    def resetdisplay(self):
        if self.curses_display.curses_display:
            self.curses_display.req_reply("Press Enter to exit and reset the screen")
            self.curses_display.__del__()

    def go(self, opponentBoard):
        """Player executes a turn.  Used by computer and human players."""
        if self.auto:
            return self.goAuto(opponentBoard)
        else:
            bombedCell = None
            bombed = False
            while bombed == False:
                bombedCell = self.getCellToBombFromPlayer(
                    opponentBoard, "Enter the cell to bomb:", '')
                if bombedCell.hit:
                    print("You chose an already bombed cell, try again")
                    continue
                opponentBoard.bombCell(bombedCell)
                self.hitMsg(bombedCell)
                bombed = True
        return opponentBoard.shipForCellIsSunk(bombedCell)

    def goAuto(self, opponentBoard):
        bombedCell:cell
        """Computer players execute a turn. If a hit is achieved, store the status and possibly some bombing targets for the next turn"""
        if self.hitState == 0:
            bombedCell = opponentBoard.bombRandomCell()
            if bombedCell != None and bombedCell.ship:
                self.hitState = 1
                self.opponentShip.append(bombedCell)
            self.hitMsg(bombedCell)

        elif self.hitState == 1:
            if opponentBoard.getCellAvail(self.opponentShip[0], "east"):
                bombedCell = opponentBoard.getCellAvail(
                    self.opponentShip[0], "east")
                if bombedCell != None and opponentBoard.bombCell(bombedCell):
                    self.hitState = 2
                    self.opponentShip.append(bombedCell)
                    if opponentBoard.getCellAvail(bombedCell, "east") != None:
                        self.attackNext.append(
                            opponentBoard.getCellAvail(bombedCell, "east"))
                    if opponentBoard.getCellAvail(self.opponentShip[0], "west") != None:
                        self.attackNext.append(opponentBoard.getCellAvail(
                            self.opponentShip[0], "west"))
                self.hitMsg(bombedCell)
            elif opponentBoard.getCellAvail(self.opponentShip[0], "north"):
                bombedCell = opponentBoard.getCellAvail(
                    self.opponentShip[0], "north")
                if bombedCell != None and opponentBoard.bombCell(bombedCell):
                    self.hitState = 2
                    self.opponentShip.append(bombedCell)
                    if opponentBoard.getCellAvail(bombedCell, "north") != None:
                        self.attackNext.append(
                            opponentBoard.getCellAvail(bombedCell, "north"))
                    if opponentBoard.getCellAvail(self.opponentShip[0], "south") != None:
                        self.attackNext.append(opponentBoard.getCellAvail(
                            self.opponentShip[0], "south"))
                self.hitMsg(bombedCell)
            # cell to east was already bombed and missed
            elif opponentBoard.getCellAvail(self.opponentShip[0], "west"):
                bombedCell = opponentBoard.getCellAvail(
                    self.opponentShip[0], "west")
                if bombedCell != None and opponentBoard.bombCell(bombedCell):
                    self.hitState = 2
                    self.opponentShip.append(bombedCell)
                    if opponentBoard.getCellAvail(bombedCell, "west") != None:
                        self.attackNext.append(
                            opponentBoard.getCellAvail(bombedCell, "west"))
                self.hitMsg(bombedCell)
            # cell to north was already bombed and missed
            elif opponentBoard.getCellAvail(self.opponentShip[0], "south"):
                bombedCell = opponentBoard.getCellAvail(
                    self.opponentShip[0], "south")
                if bombedCell != None and opponentBoard.bombCell(bombedCell):
                    self.hitState = 2
                    self.opponentShip.append(bombedCell)
                    if opponentBoard.getCellAvail(bombedCell, "south") != None:
                        self.attackNext.append(
                            opponentBoard.getCellAvail(bombedCell, "south"))
                self.hitMsg(bombedCell)

        elif self.hitState == 2 and len(self.attackNext) > 0:
            bombedCell = self.attackNext.pop()
            if type(bombedCell) is bool and len(self.attackNext) > 0:
                bombedCell = self.attackNext.pop()
            hit = opponentBoard.bombCell(bombedCell)
            self.hitMsg(bombedCell)
            if hit:
                return True

    def hitMsg(self, attackCell):
        """Print an appropriate message at the end of the turn depending on whether a hit was achieved"""
        if attackCell.ship:
            self.playerPrint(" scored a hit at " + attackCell.row+":"+attackCell.col)
        else:
            self.playerPrint(" missed")
        if self.playername != "unittest":
            time.sleep(1)

    def getCellToBombFromPlayer(self, opponentboard: board, msg: str, unitteststr: str):
        col = -1
        row = -1
        shipcell:cell
        line:str
        if unitteststr != '':
            line = unitteststr
        else:
            line = self.curses_display.req_reply(self.playername+":"+msg)
        if len(line)>= 2 and line[0] in board.rownames and line[1].lower() in board.colnames:
            return opponentboard.getCellFromIndex(self.board.getRowIndex(line[0]),self.board.getColIndex(line[1].lower()))
        else:
            self.printMsg("Invalid cell specification; try again")
            return self.getCellToBombFromPlayer(opponentboard, msg, unitteststr)


    def setName(self,name:str):
        self.playername =name