# Python code to demonstrate working of unittest 
import unittest 
from board import board,cell,ship
from player import player

class TestStringMethods(unittest.TestCase): 

	def setUp(self): 
		pass


	def checkValidShip(self,_ship,_board):
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
		_board = board('PlayerA',silent=True)
		_boardImage = _board.printBoard(False)
		self.assertIsNotNone(_boardImage)

		
		for i in range(99):
    		#horizontal alignment
			rship = _board.allocRandomShip(True)
			self.checkValidShip(rship,_board)

			#Virtical allignment
			rship = _board.allocRandomShip(False)
			self.checkValidShip(rship,_board)

		rship = _board.allocShip(False,_board.getCellFromIndex(4,3))
		self.checkValidShip(rship,_board)

		#manual placement of ships
		rship = _board.allocShip(False,_board.getCellFromIndex(0,0))
		self.checkValidShip(rship,_board)

		rship = _board.allocShip(False,_board.getCellFromIndex(7,7))
		self.checkValidShip(rship,_board)

		rship = _board.allocShip(True,_board.getCellFromIndex(0,0))
		self.checkValidShip(rship,_board)

		rship = _board.allocShip(True,_board.getCellFromIndex(7,7))
		self.checkValidShip(rship,_board)

		rship = _board.allocShip(True,_board.getCellFromIndex(4,4))
		self.assertIsNotNone(_board.getCellAvail(rship.midships,"NORTH"))
		self.assertIsNotNone(_board.getCellAvail(rship.midships,"South"))
		self.assertIsNotNone(_board.getCellAvail(rship.midships,"east"))
		self.assertIsNotNone(_board.getCellAvail(rship.midships,"weSt"))

		rship = _board.allocShip(True,_board.getCellFromIndex(0,0))
		self.assertIsNone(_board.getCellAvail(rship.bow,"NORTH"))
		self.assertIsNotNone(_board.getCellAvail(rship.bow,"South"))
		self.assertIsNotNone(_board.getCellAvail(rship.bow,"east"))
		self.assertIsNone(_board.getCellAvail(rship.bow,"weSt"))

		rship = _board.allocShip(True,_board.getCellFromIndex(7,0))
		self.assertIsNotNone(_board.getCellAvail(rship.bow,"NORTH"))
		self.assertIsNone(_board.getCellAvail(rship.bow,"South"))
		self.assertIsNotNone(_board.getCellAvail(rship.bow,"east"))
		self.assertIsNone(_board.getCellAvail(rship.bow,"weSt"))

		rship = _board.allocShip(True,_board.getCellFromIndex(0,7))
		self.assertIsNone(_board.getCellAvail(rship.stern,"NORTH"))
		self.assertIsNotNone(_board.getCellAvail(rship.stern,"South"))
		self.assertIsNone(_board.getCellAvail(rship.stern,"east"))
		self.assertIsNotNone(_board.getCellAvail(rship.stern,"weSt"))

		rship = _board.allocShip(True,_board.getCellFromIndex(7,7))
		self.assertIsNotNone(_board.getCellAvail(rship.stern,"NORTH"))
		self.assertIsNone(_board.getCellAvail(rship.stern,"South"))
		self.assertIsNone(_board.getCellAvail(rship.stern,"east"))
		self.assertIsNotNone(_board.getCellAvail(rship.stern,"weSt"))

		rship = _board.allocShip(False,_board.getCellFromIndex(0,0))
		self.assertIsNone(_board.getCellAvail(rship.bow,"NORTH"))
		self.assertIsNotNone(_board.getCellAvail(rship.stern,"South"))
		self.assertIsNotNone(_board.getCellAvail(rship.bow,"east"))
		self.assertIsNone(_board.getCellAvail(rship.bow,"weSt"))

		rship = _board.allocShip(False,_board.getCellFromIndex(0,7))
		self.assertIsNone(_board.getCellAvail(rship.bow,"NORTH"))
		self.assertIsNotNone(_board.getCellAvail(rship.stern,"South"))
		self.assertIsNone(_board.getCellAvail(rship.stern,"east"))
		self.assertIsNotNone(_board.getCellAvail(rship.stern,"weSt"))

		rship = _board.allocShip(False,_board.getCellFromIndex(7,0))
		self.assertIsNotNone(_board.getCellAvail(rship.bow,"NORTH"))
		self.assertIsNone(_board.getCellAvail(rship.stern,"South"))
		self.assertIsNotNone(_board.getCellAvail(rship.bow,"east"))
		self.assertIsNone(_board.getCellAvail(rship.bow,"weSt"))

		rship = _board.allocShip(False,_board.getCellFromIndex(7,7))
		self.assertIsNotNone(_board.getCellAvail(rship.bow,"NORTH"))
		self.assertIsNone(_board.getCellAvail(rship.stern,"South"))
		self.assertIsNone(_board.getCellAvail(rship.stern,"east"))
		self.assertIsNotNone(_board.getCellAvail(rship.stern,"weSt"))
	

	def test_bombfunctions(self):
		_board = board('unittest',silent=True)

		#should be able to bomb 64 random cells before failing
		for i in range(66):
			try:
				self.assertIsNotNone(_board.bombRandomCell())
			except:
				self.assertEqual(i,64)
				break

		_board = board('bombcells',silent=True)
		_cell = _board.bombRandomCell()
		self.assertRaises(Exception,  _board.bombRandomCell,_cell)
		self.assertRaises(Exception,  _board.bombRandomCell,None)
		_cell.hit = False
		self.assertRaises(Exception,  _board.bombRandomCell,None)
		
	def test_playerfunctions(self):
		playera = player("a",True,silent=True)
		playerb = player("b",True,silent=True)
		shipa = playera.ship
		shipb = playerb.ship
		self.assertFalse(shipa.isSunk())
		bombedCell = playera.board.bombCell(shipa.bow)
		self.assertFalse(shipa.isSunk())
		bombedCell = playera.board.bombCell(shipa.midships)
		self.assertFalse(shipa.isSunk())
		bombedCell = playera.board.bombCell(shipa.stern)
		self.assertTrue(shipa.isSunk())
		self.assertIsNotNone(playera.getCellToBombFromPlayer(playera.board,"","4a"))

		#playerb plays on own board ... doesn't matter for testing
		for i in range(10):
			playerb = player("b",True,silent=True)
			won = False
			for i in range(64):
				won =playerb.go(playerb.board)
				if won:
					break
			self.assertTrue(won)


if __name__ == '__main__':
	unittest.main() 
