from board import board
import random


class player:
    def __init__(self, playerName, auto: bool, silent=False):
        horizontal = random.randint(0, 100) % 2 == 1
        self.playername = playerName
        self.auto = auto
        self.board = board(self.playername, silent)
        self.opponentShip = []
        self.hitState = 0
        self.attackNext = []
        if self.auto:
            self.ship = self.board.allocRandomShip(horizontal)

    def go(self, opponentBoard):
        """Player executes a turn.  Used by computer and human players."""
        if self.auto:
            return self.goAuto(opponentBoard)
        else:
            bombedCell = None
            bombed = False
            while bombed == False:
                opponentBoard.printBoard(True)
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
            print(self.playername, " scored a hit at {}:{}".format(
                attackCell.col, attackCell.row))
        else:
            print(self.playername, " missed")

    def getCellToBombFromPlayer(self, _board: board, msg: str, unitteststr: str):
        col = -1
        row = -1
        line = ''
        if unitteststr == '':
            line = input(self.playername+":"+msg).lower()
        else:
            line = unitteststr
        if len(line) >= 2:
            try:
                row = _board.getRowIndex(line[0])
                col = _board.getColIndex(line[1])
            except ValueError:
                print("Invalid cell specification; try again")
                return self.getCellToBombFromPlayer(_board, msg, unitteststr)
        else:
            print("Invalid cell specification; try again")
            return self.getCellToBombFromPlayer(_board, msg, unitteststr)
        return _board.getCellFromIndex(row, col)
