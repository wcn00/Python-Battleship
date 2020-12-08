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

class ship():
    def __init__(self,horizontal, bow,midships,stern ):
        self.horizontal = horizontal
        self.bow = bow
        self.midships = midships
        self.stern = stern
    
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
        if(compasDirection.lower() == "north") and self.rownames.index(_cell.row) > 0:
            northCell = self.board[self.rownames.index(_cell.row)-1][self.colnames.index(_cell.col)]
            if northCell.hit != True :
                return northCell
        if(compasDirection.lower() == "south") and self.rownames.index(_cell.row) < 7:
            southCell = self.board[self.rownames.index(_cell.row)+1][self.colnames.index(_cell.col)]
            if southCell.hit != True :
                return southCell
            return southCell.hit
        if(compasDirection.lower() == "east") and self.colnames.index(_cell.col) < 7:
            eastCell = self.board[self.rownames.index(_cell.row)][self.colnames.index(_cell.col)+1]
            if eastCell.hit != True :
                return eastCell
        if(compasDirection.lower() == "west") and self.colnames.index(_cell.col) > 0:
            westCell = self.board[self.rownames.index(_cell.row)][self.colnames.index(_cell.col)-1]
            if westCell.hit != True :
                return westCell
        return None
    
    def printBoard(self,stdout:bool):
        boardStr = ''
        rowStr = ''
        for r,row in enumerate(self.board):
            for c,col in enumerate(row):
                rowStr += col.row+':'+col.col+','
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

        bowCell.ship = midCell.ship = sternCell.ship = True
        return ship(horizontal,bowCell,midCell,sternCell)

    #allocate a ship in any cell.  If its on the edge walk it towards the center one cell
    def allocShip(self,horizontal,shipCell:cell):
        if horizontal == True:
            if shipCell.col == 0:
                shipCell.col = shipCell.col+1
            if shipCell.col == 7:
                shipCell.col = shipCell.col - 1
            midCell = self.board[shipCell.row][shipCell.col]
            bowCell = self.board[shipCell.row][shipCell.col-1]
            sternCell = self.board[shipCell.row][shipCell.col+1]
        else:
            if shipCell.row == 0:
                shipCell.row = shipCell.row + 1
            if shipCell.row == 7:
                shipCell.row = shipCell.row - 1 
            midCell = self.board[shipCell.row][shipCell.col]
            bowCell = self.board[shipCell.row-1][shipCell.col]
            sternCell = self.board[shipCell.row+1][shipCell.col]
            
        bowCell.Ship = midCell.Ship = sternCell.Ship = True
        return ship(horizontal,bowCell,midCell,sternCell)


if __name__ == '__main__':
    boardA = board('PlayerA')
    print(boardA.printBoard(False))


