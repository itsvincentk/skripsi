# A wolf has: a board, a fitness from the board
# A wolf could do: switch board lamp position

from Board import Board
import random

class Wolf:

    def __init__(self, board, seed, punishment) -> None:
        self.board = Board(board)
        self.punishment = punishment
        random.seed(seed)

    def getEncodingDimension (self):
        return self.board.countEncodingDimension()

    # first GWO steps
    def firstGWO (self, position):
        self.position = position
        self.board.updateBoard(position, self.board.BLACK_LAMP)
        self.fitness = self.board.updateFitness(self.punishment)

    # second GWO steps
    def secondGWO (self, position):
        self.position = position
        self.board.updateBoard(position, self.board.WHITE_LAMP)
        self.fitness = self.board.updateFitness(self.punishment)

    def updateBlackPosition (self, newPosition, lampType):
        self.position = newPosition
        self.board.updateBoard(newPosition, lampType)
        self.fitness = self.board.updateFitness(self.punishment)

    # a wolf could change its lamp position
    def updatePosition (self, newPosition, lampType):
        if (lampType == Board.BLACK_LAMP):
            self.blackPosition = newPosition
        else:
            self.whitePosition = newPosition
        self.board.updateBoard(newPosition, lampType)
        self.fitness = self.board.updateFitness(self.punishment)