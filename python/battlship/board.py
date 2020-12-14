# Create a virtual battle ship board 8x8  Rows are numeric 1-8, and cols ae alpha a-h
import random
import os
from playsound import playsound
# base cell class


class cell:
    """Class used to represent a target on the board"""

    def __init__(self, col, row):
        self.row = row
        self.col = col
        self.ship = False
        self.hit = False
        self.parentship: ship
    

    def print_cell(self):
        rowStr = ''
        if self.ship and self.hit:
            rowStr += "** "
        elif self.hit:
            rowStr += "XX "
        else:
            rowStr += self.row+self.col+' '
        return rowStr


class ship():
    """Class used to represent a ship"""

    def __init__(self, bow, midships, stern):
        self.bow = bow
        self.midships = midships
        self.stern = stern
        bow.ship = midships.ship = stern.ship = True
        bow.parentship = midships.parentship = stern.parentship = self

    def isSunk(self):
        """Determine if all three cells on the ship are hit, and the ship is sunk"""
        return self.bow.hit and self.midships.hit and self.stern.hit


class board:
    colnames = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
    rownames = ('1', '2', '3', '4', '5', '6', '7', '8')

    """Class that represents a board.  Each player has a board and they are 8X8 cells in size"""
    def __init__(self, player, silent: bool):
        self.player = player
        self.silent = silent
        self.board = []
        self.opencells = []
        for r, row in enumerate(self.rownames):
            _row = []
            for c, col in enumerate(self.colnames):
                _cell = cell(col, row)
                _row.append(_cell)
                self.opencells.append(_cell)
            self.board.append(_row)

    def play_Shoot(self):
        """Play asound when a shot it taken that misses"""
        if self.silent == False:
            scriptdir = os.path.dirname(os.path.realpath(__file__))
            shoot = scriptdir + "/resources/shoot.mp3"
            playsound(shoot)

    def play_hit(self):
        """Play asound when a shot it taken that hits"""
        if self.silent == False:
            scriptdir = os.path.dirname(os.path.realpath(__file__))
            explode = scriptdir + "/resources/explosion.mp3"
            playsound(explode)

    def get_cell_avail(self, _cell, compasDirection: str):
        """If the cell in the indicated direction is not already bombed then return it"""
        if(compasDirection.lower() == "north") and self.get_row_index(_cell.row) > 0:
            northCell = self.board[self.rownames.index(
                _cell.row)-1][self.colnames.index(_cell.col)]
            if northCell.hit != True:
                return northCell
        if(compasDirection.lower() == "south") and self.get_row_index(_cell.row) < 7:
            southCell = self.board[self.rownames.index(
                _cell.row)+1][self.colnames.index(_cell.col)]
            if southCell.hit != True:
                return southCell
            return southCell.hit
        if(compasDirection.lower() == "east") and self.get_col_index(_cell.col) < 7:
            eastCell = self.board[self.rownames.index(
                _cell.row)][self.colnames.index(_cell.col)+1]
            if eastCell.hit != True:
                return eastCell
        if(compasDirection.lower() == "west") and self.get_col_index(_cell.col) > 0:
            westCell = self.board[self.rownames.index(
                _cell.row)][self.colnames.index(_cell.col)-1]
            if westCell.hit != True:
                return westCell
        return None


    def bomb_random_cell(self):
        """Bomb a cell at random. This is used by the computer players"""
        if len(self.opencells) == 0:
            raise Exception("No open cells to bomb")
        openCellNum = random.randint(0, len(self.opencells)) - 1
        c = self.opencells.pop(openCellNum)
        c.hit = True
        if c.ship:
            self.play_hit()
        return c

    def bomb_cell(self, _cell: cell):
        """Explicitly bomb a particular cell.  Used by the human playerA in manual mode"""
        if ((_cell == None) or (_cell.hit) or (self.opencells.count(_cell) != 1)):
            raise Exception("Cell is not available")
        _cell.hit = True
        self.opencells.remove(_cell)
        if _cell.ship:
            self.play_hit()
            return True
        return False

    def alloc_random_ship(self, horizontal):
        """Place a ship on the grid at random.  Used by the computer players"""
        if horizontal == True:
            colNo = random.randint(1, 6)
            rowNo = random.randint(0, 7)
            bowCell = self.board[rowNo][colNo]
            midCell = self.board[rowNo][colNo-1]
            sternCell = self.board[rowNo][colNo+1]
        else:
            colNo = random.randint(0, 7)
            rowNo = random.randint(1, 6)
            bowCell = self.board[rowNo][colNo]
            midCell = self.board[rowNo+1][colNo]
            sternCell = self.board[rowNo-1][colNo]
        return ship(bowCell, midCell, sternCell)

    def alloc_ship_by_coorid(self, horizontal, row:str,col:str):
        shipCell:cell =  self.get_cell_from_index(self.get_row_index(row),self.get_col_index(col))
        return self.alloc_ship(horizontal,shipCell)

    # allocate a ship in any cell.  If its on the edge walk it towards the center one cell
    def alloc_ship(self, horizontal, shipCell: cell):
        """Place a ship on the grid at specific coordinates.  Used by the human playerA."""
        col = self.get_col_index(shipCell.col)
        row = self.get_row_index(shipCell.row)
        if horizontal == True:
            col = self.get_col_index(shipCell.col)
            if col == 0:
                col = col+1
            if col == 7:
                col = col-1
            midCell = self.board[row][col]
            bowCell = self.board[row][col-1]
            sternCell = self.board[row][col+1]
        else:
            if row == 0:
                row = row+1
            if row == 7:
                row = row-1
            midCell = self.board[row][col]
            bowCell = self.board[row-1][col]
            sternCell = self.board[row+1][col]
        return ship(bowCell, midCell, sternCell)

    def get_col_index(self, colLbl: str):
        return board.colnames.index(colLbl)

    def get_row_index(self, rowLbl: str):
        return board.rownames.index(rowLbl)

    def get_cell_from_index(self, row, col):
        return self.board[row][col]

    def ship_for_cell_is_sunk(self, _cell: cell):
        return (_cell.ship and _cell.parentship.isSunk())
