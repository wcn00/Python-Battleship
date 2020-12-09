#Create a virtual battle ship board 8x8  Rows are numeric 1-8, and cols ae alpha a-h
import random
import os
from playsound import playsound
#base cell class
class cell:
    def __init__(self,col,row):
        self.row = row
        self.col = col
        self.ship = False
        self.hit = False
        self.parentship:ship

class ship():
    def __init__(self,horizontal, bow,midships,stern ):
        self.horizontal = horizontal
        self.bow = bow
        self.midships = midships
        self.stern = stern
        bow.ship = midships.ship = stern.ship = True
        bow.parentship = midships.parentship = stern.parentship = self
    
    def isSunk(self):
        return self.bow.hit and self.midships.hit and self.stern.hit


class board:
    def __init__(self,player,silent:bool):
        self.player = player
        self.silent = silent
        self.colnames = ('a','b','c','d','e','f','g','h')
        self.rownames = ('1','2','3','4','5','6','7','8')
        self.board = []
        self.opencells = []
        for r,row in enumerate(self.rownames):
            _row = []
            for c,col in enumerate(self.colnames):
                _cell = cell(col,row)
                _row.append(_cell)
                self.opencells.append(_cell)
            self.board.append(_row)
            

    def playShoot(self):
        if self.silent == False:
            scriptdir = os.path.dirname(os.path.realpath(__file__))
            shoot = scriptdir + "/resources/shoot.mp3"
            playsound(shoot)

    def playHit(self):
        if self.silent == False:
            scriptdir = os.path.dirname(os.path.realpath(__file__))
            explode = scriptdir + "/resources/explosion.mp3"
            playsound(explode)

    def getCellAvail(self,_cell,compasDirection:str):
        if(compasDirection.lower() == "north") and self.getRowIndex(_cell.row) > 0:
            northCell = self.board[self.rownames.index(_cell.row)-1][self.colnames.index(_cell.col)]
            if northCell.hit != True :
                return northCell
        if(compasDirection.lower() == "south") and self.getRowIndex(_cell.row) < 7:
            southCell = self.board[self.rownames.index(_cell.row)+1][self.colnames.index(_cell.col)]
            if southCell.hit != True :
                return southCell
            return southCell.hit
        if(compasDirection.lower() == "east") and self.getColIndex(_cell.col) < 7:
            eastCell = self.board[self.rownames.index(_cell.row)][self.colnames.index(_cell.col)+1]
            if eastCell.hit != True :
                return eastCell
        if(compasDirection.lower() == "west") and self.getColIndex(_cell.col) > 0:
            westCell = self.board[self.rownames.index(_cell.row)][self.colnames.index(_cell.col)-1]
            if westCell.hit != True :
                return westCell
        return None
    
    def printBoard(self,stdout:bool):
        boardStr = ''
        rowStr = ''
        for r,row in enumerate(self.board):
            for c,cell in enumerate(row):
                if cell.ship and cell.hit:
                    rowStr += "** "
                elif cell.hit:
                    rowStr += "XX "
                else:
                    rowStr += cell.row+cell.col+' '
            rowStr = rowStr[:-1]
            if(stdout):
                print(rowStr)
            boardStr += '\n'+ rowStr
            rowStr = ''
        return boardStr

    def bombRandomCell(self):
        if len(self.opencells) ==0:
            raise Exception("No open cells to bomb")
        openCellNum = random.randint(0,len(self.opencells)) -1
        c = self.opencells.pop(openCellNum)
        c.hit = True
        if c.ship:
            self.playHit()
        return c

    def bombCell(self,_cell:cell):
        if _cell == None or _cell.hit or self.opencells.count(_cell) != 1:
            raise Exception("Cell is not available")
        _cell.hit = True
        self.opencells.remove(_cell)
        if _cell.ship:
            self.playHit()
            return True
        return False
    

    def allocRandomShip(self,horizontal):
        if horizontal == True: 
            colNo = random.randint(1,6)
            rowNo = random.randint(0,7)
            bowCell = self.board[rowNo][colNo]
            midCell = self.board[rowNo][colNo-1]
            sternCell = self.board[rowNo][colNo+1]
        else:
            colNo = random.randint(0,7)
            rowNo = random.randint(1,6)
            bowCell = self.board[rowNo][colNo]
            midCell = self.board[rowNo+1][colNo]
            sternCell = self.board[rowNo-1][colNo]
        return ship(horizontal,bowCell,midCell,sternCell)

    #allocate a ship in any cell.  If its on the edge walk it towards the center one cell
    def allocShip(self,horizontal,shipCell:cell):
        col = self.getColIndex(shipCell.col);
        row = self.getRowIndex(shipCell.row);
        if horizontal == True:
            col = self.getColIndex(shipCell.col);
            if col == 0:
                col = col+1
            if col == 7:
                col = col-1
            midCell = self.board[row][col]
            bowCell = self.board[row][col-1]
            sternCell = self.board[row][col+1]
        else:
            if row == 0:
                row=row+1
            if row == 7:
                row=row-1
            midCell = self.board[row][col]
            bowCell = self.board[row-1][col]
            sternCell = self.board[row+1][col]
        return ship(horizontal,bowCell,midCell,sternCell)

    def getColIndex(self,colLbl:str):
        return self.colnames.index(colLbl);
    def getRowIndex(self,rowLbl:str):
        return self.rownames.index(rowLbl);
    def getCellFromIndex(self,row,col):
        return self.board[row][col]
    def shipForCellIsSunk(self,_cell:cell):
        return (_cell.ship and _cell.parentship.isSunk())



