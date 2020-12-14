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
                    self.shipCell = self.board.alloc_ship_by_coorid(horizontal,shipcellspec[0],shipcellspec[1].lower())
                    break;
            self.curses_display.settitle(self.playername,self.leftPlayer)
        else:
            self.board = board(self.playername, silent)
            self.ship = self.board.alloc_random_ship(horizontal)
            self.curses_display.settitle(self.playername,self.leftPlayer)

    def print_board(self):
        self.curses_display.display_board(self.playername,self.board,self.leftPlayer)
        
    def print_msg(self,msg:str):
        self.curses_display.print_status(msg)

    def player_print(self,msg:str):
        self.curses_display.print_status(self.playername+": "+msg)
        
    def resetdisplay(self):
        if self.curses_display.curses_display:
            time.sleep(5)
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
                bombedCell = self.get_cell_to_bomb_from_player(
                    opponentBoard, "Enter the cell to bomb:", '')
                if bombedCell.hit:
                    print("You chose an already bombed cell, try again")
                    continue
                opponentBoard.bomb_cell(bombedCell)
                self.hit_msg(bombedCell)
                bombed = True
        return opponentBoard.ship_for_cell_is_sunk(bombedCell)

    def goAuto(self, opponentBoard):
        bombedCell:cell
        """Computer players execute a turn. If a hit is achieved, store the status and possibly some bombing targets for the next turn"""
        if self.hitState == 0:
            bombedCell = opponentBoard.bomb_random_cell()
            if bombedCell != None and bombedCell.ship:
                self.hitState = 1
                self.opponentShip.append(bombedCell)
            self.hit_msg(bombedCell)

        elif self.hitState == 1:
            if opponentBoard.get_cell_avail(self.opponentShip[0], "east"):
                bombedCell = opponentBoard.get_cell_avail(
                    self.opponentShip[0], "east")
                if bombedCell != None and opponentBoard.bomb_cell(bombedCell):
                    self.hitState = 2
                    self.opponentShip.append(bombedCell)
                    if opponentBoard.get_cell_avail(bombedCell, "east") != None:
                        self.attackNext.append(
                            opponentBoard.get_cell_avail(bombedCell, "east"))
                    if opponentBoard.get_cell_avail(self.opponentShip[0], "west") != None:
                        self.attackNext.append(opponentBoard.get_cell_avail(
                            self.opponentShip[0], "west"))
                self.hit_msg(bombedCell)
            elif opponentBoard.get_cell_avail(self.opponentShip[0], "north"):
                bombedCell = opponentBoard.get_cell_avail(
                    self.opponentShip[0], "north")
                if bombedCell != None and opponentBoard.bomb_cell(bombedCell):
                    self.hitState = 2
                    self.opponentShip.append(bombedCell)
                    if opponentBoard.get_cell_avail(bombedCell, "north") != None:
                        self.attackNext.append(
                            opponentBoard.get_cell_avail(bombedCell, "north"))
                    if opponentBoard.get_cell_avail(self.opponentShip[0], "south") != None:
                        self.attackNext.append(opponentBoard.get_cell_avail(
                            self.opponentShip[0], "south"))
                self.hit_msg(bombedCell)
            # cell to east was already bombed and missed
            elif opponentBoard.get_cell_avail(self.opponentShip[0], "west"):
                bombedCell = opponentBoard.get_cell_avail(
                    self.opponentShip[0], "west")
                if bombedCell != None and opponentBoard.bomb_cell(bombedCell):
                    self.hitState = 2
                    self.opponentShip.append(bombedCell)
                    if opponentBoard.get_cell_avail(bombedCell, "west") != None:
                        self.attackNext.append(
                            opponentBoard.get_cell_avail(bombedCell, "west"))
                self.hit_msg(bombedCell)
            # cell to north was already bombed and missed
            elif opponentBoard.get_cell_avail(self.opponentShip[0], "south"):
                bombedCell = opponentBoard.get_cell_avail(
                    self.opponentShip[0], "south")
                if bombedCell != None and opponentBoard.bomb_cell(bombedCell):
                    self.hitState = 2
                    self.opponentShip.append(bombedCell)
                    if opponentBoard.get_cell_avail(bombedCell, "south") != None:
                        self.attackNext.append(
                            opponentBoard.get_cell_avail(bombedCell, "south"))
                self.hit_msg(bombedCell)

        elif self.hitState == 2 and len(self.attackNext) > 0:
            bombedCell = self.attackNext.pop()
            if type(bombedCell) is bool and len(self.attackNext) > 0:
                bombedCell = self.attackNext.pop()
            hit = opponentBoard.bomb_cell(bombedCell)
            self.hit_msg(bombedCell)
            if hit:
                return True

    def hit_msg(self, attackCell):
        """Print an appropriate message at the end of the turn depending on whether a hit was achieved"""
        if attackCell.ship:
            self.player_print(" scored a hit at " + attackCell.row+":"+attackCell.col)
        else:
            self.player_print(" missed")
        if self.playername != "unittest":
            time.sleep(1)

    def get_cell_to_bomb_from_player(self, opponentboard: board, msg: str, unitteststr: str):
        col = -1
        row = -1
        shipcell:cell
        line:str
        if unitteststr != '':
            line = unitteststr
        else:
            line = self.curses_display.req_reply(self.playername+":"+msg)
        if len(line)>= 2 and line[0] in board.rownames and line[1].lower() in board.colnames:
            return opponentboard.get_cell_from_index(self.board.get_row_index(line[0]),self.board.get_col_index(line[1].lower()))
        else:
            self.print_msg("Invalid cell specification; try again")
            return self.get_cell_to_bomb_from_player(opponentboard, msg, unitteststr)


    def set_name(self,name:str):
        self.playername =name