# Python code to demonstrate working of unittest
import unittest
from board import board, cell, ship
from player import player
from display import display


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        pass

    def checkValidShip(self, _ship, _board):
        self.assertIn(_ship.midships.row, _board.rownames)
        self.assertIn(_ship.midships.col, _board.colnames)
        self.assertIn(_ship.bow.row, _board.rownames)
        self.assertIn(_ship.bow.col, _board.colnames)
        self.assertIn(_ship.stern.col, _board.colnames)
        self.assertIn(_ship.stern.row, _board.rownames)

        self.assertTrue(_ship.bow.ship)
        self.assertTrue(_ship.stern.ship)
        self.assertTrue(_ship.midships.ship)
        self.assertFalse(_ship.isSunk())

    # Returns True if the string contains 4 a.

    def test_boardfunctions(self):
        self.maxDiff = None
        _board = board('PlayerA', silent=True)

        for i in range(99):
            # horizontal alignment
            rship = _board.alloc_random_ship(True)
            self.checkValidShip(rship, _board)

            # Virtical allignment
            rship = _board.alloc_random_ship(False)
            self.checkValidShip(rship, _board)

        rship = _board.alloc_ship(False, _board.get_cell_from_index(4, 3))
        self.checkValidShip(rship, _board)

        # manual placement of ships
        rship = _board.alloc_ship(False, _board.get_cell_from_index(0, 0))
        self.checkValidShip(rship, _board)

        rship = _board.alloc_ship(False, _board.get_cell_from_index(7, 7))
        self.checkValidShip(rship, _board)

        rship = _board.alloc_ship(True, _board.get_cell_from_index(0, 0))
        self.checkValidShip(rship, _board)

        rship = _board.alloc_ship(True, _board.get_cell_from_index(7, 7))
        self.checkValidShip(rship, _board)

        rship = _board.alloc_ship(True, _board.get_cell_from_index(4, 4))
        self.assertIsNotNone(_board.get_cell_avail(rship.midships, "NORTH"))
        self.assertIsNotNone(_board.get_cell_avail(rship.midships, "South"))
        self.assertIsNotNone(_board.get_cell_avail(rship.midships, "east"))
        self.assertIsNotNone(_board.get_cell_avail(rship.midships, "weSt"))

        rship = _board.alloc_ship(True, _board.get_cell_from_index(0, 0))
        self.assertIsNone(_board.get_cell_avail(rship.bow, "NORTH"))
        self.assertIsNotNone(_board.get_cell_avail(rship.bow, "South"))
        self.assertIsNotNone(_board.get_cell_avail(rship.bow, "east"))
        self.assertIsNone(_board.get_cell_avail(rship.bow, "weSt"))

        rship = _board.alloc_ship(True, _board.get_cell_from_index(7, 0))
        self.assertIsNotNone(_board.get_cell_avail(rship.bow, "NORTH"))
        self.assertIsNone(_board.get_cell_avail(rship.bow, "South"))
        self.assertIsNotNone(_board.get_cell_avail(rship.bow, "east"))
        self.assertIsNone(_board.get_cell_avail(rship.bow, "weSt"))

        rship = _board.alloc_ship(True, _board.get_cell_from_index(0, 7))
        self.assertIsNone(_board.get_cell_avail(rship.stern, "NORTH"))
        self.assertIsNotNone(_board.get_cell_avail(rship.stern, "South"))
        self.assertIsNone(_board.get_cell_avail(rship.stern, "east"))
        self.assertIsNotNone(_board.get_cell_avail(rship.stern, "weSt"))

        rship = _board.alloc_ship(True, _board.get_cell_from_index(7, 7))
        self.assertIsNotNone(_board.get_cell_avail(rship.stern, "NORTH"))
        self.assertIsNone(_board.get_cell_avail(rship.stern, "South"))
        self.assertIsNone(_board.get_cell_avail(rship.stern, "east"))
        self.assertIsNotNone(_board.get_cell_avail(rship.stern, "weSt"))

        rship = _board.alloc_ship(False, _board.get_cell_from_index(0, 0))
        self.assertIsNone(_board.get_cell_avail(rship.bow, "NORTH"))
        self.assertIsNotNone(_board.get_cell_avail(rship.stern, "South"))
        self.assertIsNotNone(_board.get_cell_avail(rship.bow, "east"))
        self.assertIsNone(_board.get_cell_avail(rship.bow, "weSt"))

        rship = _board.alloc_ship(False, _board.get_cell_from_index(0, 7))
        self.assertIsNone(_board.get_cell_avail(rship.bow, "NORTH"))
        self.assertIsNotNone(_board.get_cell_avail(rship.stern, "South"))
        self.assertIsNone(_board.get_cell_avail(rship.stern, "east"))
        self.assertIsNotNone(_board.get_cell_avail(rship.stern, "weSt"))

        rship = _board.alloc_ship(False, _board.get_cell_from_index(7, 0))
        self.assertIsNotNone(_board.get_cell_avail(rship.bow, "NORTH"))
        self.assertIsNone(_board.get_cell_avail(rship.stern, "South"))
        self.assertIsNotNone(_board.get_cell_avail(rship.bow, "east"))
        self.assertIsNone(_board.get_cell_avail(rship.bow, "weSt"))

        rship = _board.alloc_ship(False, _board.get_cell_from_index(7, 7))
        self.assertIsNotNone(_board.get_cell_avail(rship.bow, "NORTH"))
        self.assertIsNone(_board.get_cell_avail(rship.stern, "South"))
        self.assertIsNone(_board.get_cell_avail(rship.stern, "east"))
        self.assertIsNotNone(_board.get_cell_avail(rship.stern, "weSt"))

    def test_bombfunctions(self):
        _board = board('unittest', silent=True)

        # should be able to bomb 64 random cells before failing
        for i in range(66):
            try:
                self.assertIsNotNone(_board.bomb_random_cell())
            except:
                self.assertEqual(i, 64)
                break

        _board = board('bombcells', silent=True)
        _cell = _board.bomb_random_cell()
        self.assertRaises(Exception,  _board.bomb_random_cell, _cell)
        self.assertRaises(Exception,  _board.bomb_random_cell, None)
        _cell.hit = False
        self.assertRaises(Exception,  _board.bomb_random_cell, None)

    def test_playerfunctions(self):
        curses_display = display(False)
        playera = player("unittest", curses_display,silent=True,autoPlay=True,leftPlayer=True)
        playerb = player("unittest", curses_display,silent=True,autoPlay=True,leftPlayer=False)
        shipa = playera.ship
        shipb = playerb.ship
        self.assertFalse(shipa.isSunk())
        bombedCell = playera.board.bomb_cell(shipa.bow)
        self.assertFalse(shipa.isSunk())
        bombedCell = playera.board.bomb_cell(shipa.midships)
        self.assertFalse(shipa.isSunk())
        bombedCell = playera.board.bomb_cell(shipa.stern)
        self.assertTrue(shipa.isSunk())
        self.assertIsNotNone(
            playera.get_cell_to_bomb_from_player(playera.board, "", "4a"))
        try:
            playerb.print_board()
            playerb.print_msg("mary had a little lamb")
            playerb.player_print("mary had a little lamb")
            playerb.set_name("walter")
            shipb  = playerb.board.alloc_ship_by_coorid(True,'4','b')
            self.assertIsNotNone(shipb)
        except:
            self.assertTrue(False)

        # playerb plays on own board ... doesn't matter for testing
        for i in range(10):
            playerb = player("unittest", curses_display,silent=True,autoPlay=True,leftPlayer=False)
            won = False
            for i in range(64):
                won = playerb.go(playerb.board)
                if won:
                    break
            self.assertTrue(won)

    def test_displayfunctions(self):
        curses_display = display(False)
        _board = board('unittest', silent=True)
        self.assertIsNotNone(curses_display)
        try:
            curses_display.display_board("unittest",_board,True)
            curses_display.print_status("mary had a little lamb")
        except Exception:            
            self.assertTrue(False)

        
        curses_display.__del__()


if __name__ == '__main__':
    unittest.main()
