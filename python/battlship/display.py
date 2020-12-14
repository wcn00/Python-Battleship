import curses
from board import board
from curses.textpad import Textbox, rectangle
import os


class display:
    """Create a display with two boards and a status/input area"""
    def __init__(self,curses_display):
        self.displayA = None
        self.displayB = None
        self.status = None
        self.inputarea = None
        window = None
        self.curses_display = curses_display
        if os.name == 'posix':
            os.system('clear')
        else:
            # for windows platfrom
            os.system('cls')
        if curses_display:
            window = curses.initscr()
            curses.savetty()
            curses.echo(False)
            self.titleA = curses.newwin(10,24,4,5)
            self.titleB = curses.newwin(10,24,4,35)
            self.titleA.addstr("Player A")
            self.titleA.refresh()
            self.titleB.addstr("Player B")
            self.titleB.refresh()
            self.displayA = curses.newwin(10,24,5,5)
            self.displayB = curses.newwin(10,24,5,35)
            self.status = curses.newwin(1,80,14,1)
            self.inputarea = curses.newwin(1,80,16,1)

   # print out some text


    def __del__(self):
        """return the terminal to its normal config"""
        if self.curses_display:
            curses.echo(True)
            curses.resetty()
            curses.endwin()

    def printBoard(self,playername:str,bd:board,leftPlayer:bool):
        if not self.curses_display:
            self._printtty(playername,bd)
            return
        if leftPlayer:
            self.displayA.clear()
        else:
            self.displayB.clear()
        for row in bd.board:
            boardrow=''
            for cell in row:
                boardrow +=cell.printCell()
            if leftPlayer:
                self.displayA.addstr(boardrow)
                self.displayA.refresh()
            else:
                self.displayB.addstr(boardrow)
                self.displayB.refresh()

    def settitle(self,title:str,leftPlayer:bool):
        if self.curses_display:
            if leftPlayer:
                self.titleA.clear()
                self.titleA.addstr(title)
                self.titleA.refresh()
            else:
                self.titleB.clear()
                self.titleB.addstr(title)
                self.titleB.refresh()


    def _printtty(self,playername,bd):
        print("Board for player: "+playername)
        for row in bd.board:
            boardrow=''
            for cell in row:
                boardrow +=cell.printCell()
            print(boardrow)
        print("\n")
            
               

    def req_reply(self,req:str):
        if self.curses_display:
            return self.req_reply_curses(req)
        else:
            return input(req)
    
    def print_status(self,req:str):
        if self.curses_display:
            self.print_status_curses(req)
        else:
            print(req)

    def req_reply_curses(self,req:str):
        self.status.clear()
        self.status.addstr(req)
        self.status.refresh()
        resp = ''
        self.inputarea.clear()
        curses.echo(False)
        box = Textbox(self.inputarea)
        box.edit()
        return box.gather()


    def print_status_curses(self,req:str):
        self.status.clear()
        self.status.addstr(req)
        self.status.refresh()
