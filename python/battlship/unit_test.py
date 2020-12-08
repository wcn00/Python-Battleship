# Python code to demonstrate working of unittest 
import unittest 
from board import board,cell,ship
from player import player

boardImage = "\n1:a,1:b,1:c,1:d,1:e,1:f,1:g,1:h\n2:a,2:b,2:c,2:d,2:e,2:f,2:g,2:h\n3:a,3:b,3:c,3:d,3:e,3:f,3:g,3:h\n4:a,4:b,4:c,4:d,4:e,4:f,4:g,4:h\n5:a,5:b,5:c,5:d,5:e,5:f,5:g,5:h\n6:a,6:b,6:c,6:d,6:e,6:f,6:g,6:h\n7:a,7:b,7:c,7:d,7:e,7:f,7:g,7:h\n8:a,8:b,8:c,8:d,8:e,8:f,8:g,8:h"
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
		_board = board('PlayerA')
		_boardImage = _board.printBoard(False)
		self.assertEqual(_boardImage,boardImage)

		
		for i in range(99):
    		#horizontal alignment
			rship = _board.allocRandomShip(True)
			self.checkValidShip(rship,_board)

			#Virtical allignment
			rship = _board.allocRandomShip(False)
			self.checkValidShip(rship,_board)

		rship = _board.allocShip(False,cell(3,4))
		self.checkValidShip(rship,_board)

		#manual placement of ships
		rship = _board.allocShip(False,cell(0,0))
		self.checkValidShip(rship,_board)

		rship = _board.allocShip(False,cell(7,7))
		self.checkValidShip(rship,_board)

		rship = _board.allocShip(True,cell(0,0))
		self.checkValidShip(rship,_board)

		rship = _board.allocShip(True,cell(7,7))
		self.checkValidShip(rship,_board)

		rship = _board.allocShip(True,cell(4,4))
		self.assertIsNotNone(_board.getCellAvail(rship.midships,"NORTH"))
		self.assertIsNotNone(_board.getCellAvail(rship.midships,"South"))
		self.assertIsNotNone(_board.getCellAvail(rship.midships,"east"))
		self.assertIsNotNone(_board.getCellAvail(rship.midships,"weSt"))

		rship = _board.allocShip(True,cell(0,0))
		self.assertIsNone(_board.getCellAvail(rship.bow,"NORTH"))
		self.assertIsNotNone(_board.getCellAvail(rship.bow,"South"))
		self.assertIsNotNone(_board.getCellAvail(rship.bow,"east"))
		self.assertIsNone(_board.getCellAvail(rship.bow,"weSt"))

		rship = _board.allocShip(True,cell(0,7))
		self.assertIsNotNone(_board.getCellAvail(rship.bow,"NORTH"))
		self.assertIsNone(_board.getCellAvail(rship.bow,"South"))
		self.assertIsNotNone(_board.getCellAvail(rship.bow,"east"))
		self.assertIsNone(_board.getCellAvail(rship.bow,"weSt"))

		rship = _board.allocShip(True,cell(7,0))
		self.assertIsNone(_board.getCellAvail(rship.stern,"NORTH"))
		self.assertIsNotNone(_board.getCellAvail(rship.stern,"South"))
		self.assertIsNone(_board.getCellAvail(rship.stern,"east"))
		self.assertIsNotNone(_board.getCellAvail(rship.stern,"weSt"))

		rship = _board.allocShip(True,cell(7,7))
		self.assertIsNotNone(_board.getCellAvail(rship.stern,"NORTH"))
		self.assertIsNone(_board.getCellAvail(rship.stern,"South"))
		self.assertIsNone(_board.getCellAvail(rship.stern,"east"))
		self.assertIsNotNone(_board.getCellAvail(rship.stern,"weSt"))

		rship = _board.allocShip(False,cell(0,0))
		self.assertIsNone(_board.getCellAvail(rship.bow,"NORTH"))
		self.assertIsNotNone(_board.getCellAvail(rship.bow,"South"))
		self.assertIsNotNone(_board.getCellAvail(rship.bow,"east"))
		self.assertIsNone(_board.getCellAvail(rship.bow,"weSt"))

		rship = _board.allocShip(False,cell(0,7))
		self.assertIsNotNone(_board.getCellAvail(rship.stern,"NORTH"))
		self.assertIsNone(_board.getCellAvail(rship.stern,"South"))
		self.assertIsNotNone(_board.getCellAvail(rship.stern,"east"))
		self.assertIsNone(_board.getCellAvail(rship.stern,"weSt"))

		rship = _board.allocShip(False,cell(7,0))
		self.assertIsNone(_board.getCellAvail(rship.bow,"NORTH"))
		self.assertIsNotNone(_board.getCellAvail(rship.bow,"South"))
		self.assertIsNone(_board.getCellAvail(rship.bow,"east"))
		self.assertIsNotNone(_board.getCellAvail(rship.bow,"weSt"))

		rship = _board.allocShip(False,cell(7,7))
		self.assertIsNotNone(_board.getCellAvail(rship.stern,"NORTH"))
		self.assertIsNone(_board.getCellAvail(rship.stern,"South"))
		self.assertIsNone(_board.getCellAvail(rship.stern,"east"))
		self.assertIsNotNone(_board.getCellAvail(rship.stern,"weSt"))
	

	def test_bombfunctions(self):
		_board = board('unittest')

		#should be able to bomb 64 random cells before failing
		for i in range(66):
			try:
				self.assertIsNotNone(_board.bombRandomCell())
			except:
				self.assertEqual(i,64)
				break

		_board = board('bombcells')
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

		#playerb plays on own board ... doesn't matter for testing
		won = False
		for i in range(64):
			won =playerb.go(playerb.board)
			if won:
				break
		self.assertTrue(won)


if __name__ == '__main__':
	unittest.main() 
