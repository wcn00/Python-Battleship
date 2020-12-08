from board import board
import random

class player:
    def __init__(self,playerName,auto:bool,silent=False):
        horizontal = random.randint(0,100)%2 == 1
        self.playername = playerName
        self.board = board(self.playername,silent)
        self.ship = self.board.allocRandomShip(horizontal)
        self.opponentShip = []
        self.hitState = 0
        self.attackNext = []


    def go(self,opponentBoard):
        if self.hitState == 0:
            bombedCell = opponentBoard.bombRandomCell()
            if bombedCell!=None and bombedCell.ship:
                self.hitState = 1;
                self.opponentShip.append(bombedCell)
            self.hitMsg(bombedCell)
        
        elif self.hitState == 1 :
            if opponentBoard.getCellAvail(self.opponentShip[0], "east"):
                bombedCell = opponentBoard.getCellAvail(self.opponentShip[0], "east")
                if bombedCell != None and opponentBoard.bombCell(bombedCell):
                    self.hitState = 2;
                    self.opponentShip.append(bombedCell)
                    if opponentBoard.getCellAvail(bombedCell,"east") != None:
                        self.attackNext.append(opponentBoard.getCellAvail(bombedCell,"east"))
                    if  opponentBoard.getCellAvail(self.opponentShip[0], "west") != None:
                        self.attackNext.append(opponentBoard.getCellAvail(self.opponentShip[0],"west"))
                self.hitMsg(bombedCell)
            elif opponentBoard.getCellAvail(self.opponentShip[0], "north"):
                bombedCell = opponentBoard.getCellAvail(self.opponentShip[0], "north")
                if bombedCell != None and opponentBoard.bombCell(bombedCell):
                    self.hitState = 2;
                    self.opponentShip.append(bombedCell)
                    if opponentBoard.getCellAvail(bombedCell,"north") != None:
                        self.attackNext.append(opponentBoard.getCellAvail(bombedCell,"north"))
                    if  opponentBoard.getCellAvail(self.opponentShip[0], "south") != None:
                        self.attackNext.append(opponentBoard.getCellAvail(self.opponentShip[0],"south"))
                self.hitMsg(bombedCell)
            elif opponentBoard.getCellAvail(self.opponentShip[0], "west"): #cell to east was already bombed and missed
                bombedCell = opponentBoard.getCellAvail(self.opponentShip[0], "west")
                if bombedCell != None and opponentBoard.bombCell(bombedCell):
                    self.hitState = 2;
                    self.opponentShip.append(bombedCell)
                    if  opponentBoard.getCellAvail(bombedCell, "west") != None:
                        self.attackNext.append(opponentBoard.getCellAvail(bombedCell,"west"))
                self.hitMsg(bombedCell)
            elif opponentBoard.getCellAvail(self.opponentShip[0], "south") : #cell to north was already bombed and missed
                bombedCell = opponentBoard.getCellAvail(self.opponentShip[0], "south")
                if bombedCell != None and opponentBoard.bombCell(bombedCell):
                    self.hitState = 2;
                    self.opponentShip.append(bombedCell)
                    if opponentBoard.getCellAvail(bombedCell,"south") != None:
                        self.attackNext.append(opponentBoard.getCellAvail(bombedCell,"south"))
                self.hitMsg(bombedCell)
        elif self.hitState==2 and len(self.attackNext) > 0:
            bombedCell = self.attackNext.pop();
            self.hitMsg(bombedCell)
            if opponentBoard.bombCell(bombedCell):
                return True
        
    def hitMsg(self,attackCell):
        if attackCell.ship :
            print(self.playername," scored a hit at {}:{}".format(attackCell.col,attackCell.row))
        else:
            print(self.playername," missed")

            
    
