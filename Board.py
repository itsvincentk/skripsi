# A board is owned by a wolf

import numpy as np
from Cell import Cell


class Board:
    # Board sizes
    SIZE_LEVEL_7 = 7
    SIZE_LEVEL_10 = 10
    SIZE_LEVEL_14 = 14
    SIZE_LEVEL_25 = 25
    SIZE_DAILY = 30
    SIZE_WEEKLY = 30
    SIZE_MONTHLY = 40

    # Difficulty
    DIFF_EASY = 'easy'
    DIFF_NORMAL = 'normal'
    DIFF_HARD = 'hard'
    DIFF_DAILY = 'daily'
    DIFF_WEEKLY = 'weekly'
    DIFF_MONTHLY = 'monthly'

    BLACK_LAMP = 0
    WHITE_LAMP = 1

    def __init__(self, board) -> None:
        self.board = np.array(board)
        self.originalBoard = np.array(board)
        size = self.board.shape
        self.rowSize = size[0]
        self.colSize = size[1]

    # update board lamp position
    def updateBoard (self, position, lampType):
        self.board = self.originalBoard.copy()
        if lampType == self.BLACK_LAMP:
            self.putBlackLamps(position)
        elif lampType == self.WHITE_LAMP:
            self.putWhiteLamps(position)

    def copyBoard (self):
        self.originalBoard = self.board.copy()

    def putBlackLamps (self, position):
        # move = [[1, 0, -1, 0],[0, 1, 0, -1]] # x, y
        for i, black in enumerate (self.blackPosition):
            rowPos = black[0]
            colPos = black[1]
            if (self.board[rowPos][colPos] == Cell.BLACK_ONE):
                if (position[i] == 0):
                    self.putSingleLamp(rowPos, colPos+1)
                elif (position[i] == 1):
                    self.putSingleLamp(rowPos+1, colPos)
                elif (position[i] == 2):
                    self.putSingleLamp(rowPos, colPos-1)
                elif (position[i] == 3):
                    self.putSingleLamp(rowPos-1, colPos)
            elif (self.board[rowPos][colPos] == Cell.BLACK_TWO):
                if (position[i] == 0):
                    self.putSingleLamp(rowPos, colPos+1)
                    self.putSingleLamp(rowPos+1, colPos)
                elif (position[i] == 1):
                    self.putSingleLamp(rowPos+1, colPos)
                    self.putSingleLamp(rowPos, colPos-1)
                elif (position[i] == 2):
                    self.putSingleLamp(rowPos, colPos-1)
                    self.putSingleLamp(rowPos-1, colPos)
                elif (position[i] == 3):
                    self.putSingleLamp(rowPos-1, colPos)
                    self.putSingleLamp(rowPos, colPos+1)
                elif (position[i] == 4):
                    self.putSingleLamp(rowPos, colPos+1)
                    self.putSingleLamp(rowPos, colPos-1)
                elif (position[i] == 5):
                    self.putSingleLamp(rowPos+1, colPos)
                    self.putSingleLamp(rowPos-1, colPos)
            elif (self.board[rowPos][colPos] == Cell.BLACK_THREE):
                if (position[i] == 0):
                    self.putSingleLamp(rowPos, colPos+1)
                    self.putSingleLamp(rowPos+1, colPos)
                    self.putSingleLamp(rowPos, colPos-1)
                elif (position[i] == 1):
                    self.putSingleLamp(rowPos+1, colPos)
                    self.putSingleLamp(rowPos, colPos-1)
                    self.putSingleLamp(rowPos-1, colPos)
                elif (position[i] == 2):
                    self.putSingleLamp(rowPos, colPos-1)
                    self.putSingleLamp(rowPos-1, colPos)
                    self.putSingleLamp(rowPos, colPos+1)
                elif (position[i] == 3):
                    self.putSingleLamp(rowPos-1, colPos)
                    self.putSingleLamp(rowPos, colPos+1)
                    self.putSingleLamp(rowPos+1, colPos)
            elif (self.board[rowPos][colPos] == Cell.BLACK_FOUR):
                self.putSingleLamp(rowPos, colPos+1)
                self.putSingleLamp(rowPos+1, colPos)
                self.putSingleLamp(rowPos, colPos-1)
                self.putSingleLamp(rowPos-1, colPos)

    def putWhiteLamps (self, position):
        for i, white in enumerate (self.whitePosition):
            rowPos = white[0]
            colPos = white[1]
            if (position[i] == 1):
                self.putSingleLamp(rowPos, colPos)

    # update board fitness -- basically count the board fitness
    # punishment yang baru dipake cuman w1 -- w3, w4 sama w5 belum di develop
    def updateFitness (self, punishments):
        movement = [[0, 1, 0, -1], [1, 0, -1, 0]]
        collision = 0
        whiteTiles = 0
        blackLamp = 0
        fitness = 0
        centerWhite = 0
        endBlack = 0
        for i in range (self.rowSize):
            for j in range (self.colSize):
                if (self.board[i][j] == Cell.WHITE_EMPTY or self.board[i][j] == Cell.FORBIDDEN):
                    whiteTiles += 1
                    check = True
                    for k in range (4):
                        nextRow = i + movement[0][k]
                        nextCol = j + movement[1][k]
                        if (nextRow >= 0 and nextCol >= 0 and nextRow < self.rowSize and nextCol < self.colSize):
                            if (self.board[nextRow][nextCol] > Cell.BLACK_ANY):
                                check = False
                    if (check): centerWhite += 1
                elif (self.board[i][j] == Cell.COLLISION):
                    collision += 1
                elif (self.board[i][j] <= Cell.BLACK_FOUR or self.board[i][j] > Cell.FORBIDDEN):
                    lampCount = 0
                    blackNumber = self.board[i][j]
                    if (self.board[i][j] > Cell.FORBIDDEN): blackNumber = self.board[i][j] / 100
                    for k in range (4):
                        nextRow = i + movement[0][k]
                        nextCol = j + movement[1][k]
                        if (nextRow >= 0 and nextCol >= 0 and nextRow < self.rowSize and nextCol < self.colSize):
                            if (self.board[nextRow][nextCol] == Cell.LAMP or self.board[nextRow][nextCol] == Cell.COLLISION):
                                lampCount += 1
                    if (abs(blackNumber - lampCount) > 0):
                        blackLamp += 1
                        # cek ujung
                        if ((i == 0 and (j == self.colSize-1 or j == 0)) or (i == self.rowSize-1 and (j == self.colSize-1 or j == 0))):
                             if (self.board[i][j] == Cell.BLACK_TWO):
                                endBlack += 1
                        # cek tepi
                        if (((i == 0 or i == self.rowSize-1) and (j < self.colSize-1 and j > 0)) or ((j == 0 or j == self.colSize-1) and (i < self.rowSize-1 and i > 0))):
                            if (self.board[i][j] == Cell.BLACK_THREE):
                                endBlack += 1
        fitness += (collision * punishments[0] + blackLamp * punishments[1] + whiteTiles * punishments[2] + endBlack * punishments[3] + centerWhite * punishments[4])
        self.violation = [collision, whiteTiles, blackLamp, centerWhite, endBlack]
        # print (self.board)
        # print ("COLLISION = ", collision)
        # print ("BLACK LAMP = ", blackLamp)
        # print ("WHITE TILES = ", whiteTiles)
        # print ("END BLACK = ", endBlack)
        # print ("CENTER WHITE = ", centerWhite)
        return fitness

    # put a lamp on (row, col) board position
    def putSingleLamp (self, rowPos, colPos):

        if (rowPos < 0 or rowPos >= self.rowSize or colPos < 0 or colPos >= self.colSize):
            return False
    
        if (self.board[rowPos][colPos] == Cell.LAMP or self.board[rowPos][colPos] <= Cell.BLACK_ANY or self.board[rowPos][colPos] >= Cell.FORBIDDEN):
            return False
        
        # put lamp on position
        if (self.board[rowPos][colPos] == Cell.YELLOW):
            self.board[rowPos][colPos] = Cell.COLLISION
        else: 
            self.board[rowPos][colPos] = Cell.LAMP

        # light rightside
        for i in range (colPos+1, self.colSize):
            if (i >= 0 and i < self.colSize):
                if (self.board[rowPos][i] <= Cell.BLACK_ANY or self.board[rowPos][i] > Cell.FORBIDDEN):
                    break
                elif (self.board[rowPos][i] == Cell.WHITE_EMPTY or self.board[rowPos][i] == Cell.FORBIDDEN):
                    self.board[rowPos][i] = Cell.YELLOW
                elif (self.board[rowPos][i] == Cell.LAMP):
                    self.board[rowPos][i] = Cell.COLLISION

        # light leftside
        for i in range (colPos-1, -1, -1):
            if (i >= 0 and i < self.colSize):
                if (self.board[rowPos][i] <= Cell.BLACK_ANY or self.board[rowPos][i] > Cell.FORBIDDEN):
                    break
                elif (self.board[rowPos][i] == Cell.WHITE_EMPTY or self.board[rowPos][i] == Cell.FORBIDDEN):
                    self.board[rowPos][i] = Cell.YELLOW
                elif (self.board[rowPos][i] == Cell.LAMP):
                    self.board[rowPos][i] = Cell.COLLISION
        
        # light downside
        for i in range (rowPos+1, self.rowSize):
            if (i >= 0 and i < self.rowSize):
                if (self.board[i][colPos] <= Cell.BLACK_ANY or self.board[i][colPos] > Cell.FORBIDDEN):
                    break
                elif (self.board[i][colPos] == Cell.WHITE_EMPTY or self.board[i][colPos] == Cell.FORBIDDEN):
                    self.board[i][colPos] = Cell.YELLOW
                elif (self.board[i][colPos] == Cell.LAMP):
                    self.board[i][colPos] = Cell.COLLISION

        # light upside
        for i in range (rowPos-1, -1, -1):
            if (i >= 0 and i < self.rowSize):
                if (self.board[i][colPos] <= Cell.BLACK_ANY or self.board[i][colPos] > Cell.FORBIDDEN):
                    break
                elif (self.board[i][colPos] == Cell.WHITE_EMPTY or self.board[i][colPos] == Cell.FORBIDDEN):
                    self.board[i][colPos] = Cell.YELLOW
                elif (self.board[i][colPos] == Cell.LAMP):
                    self.board[i][colPos] = Cell.COLLISION

    # find all black 1--4 coordinates, maxCombinationOnBlack
    def countEncodingDimension (self):
        movement = [[0, 1, 0, -1], [1, 0, -1, 0]]
        maxBlack = []
        blackPosition = []
        whitePosition = []
        for i in range (self.rowSize):
            for j in range (self.colSize):
                # get all black 1--4
                if (self.board[i][j] <= Cell.BLACK_FOUR and self.board[i][j] > Cell.BLACK_ZERO):
                    blackPosition.append([i, j])
                    # max combination number on black 1--4
                    if (self.board[i][j] == Cell.BLACK_ONE):
                        maxBlack.append(3)
                    elif (self.board[i][j] == Cell.BLACK_TWO):
                        maxBlack.append(5)
                    elif (self.board[i][j] == Cell.BLACK_THREE):
                        maxBlack.append(3)
                    elif (self.board[i][j] == Cell.BLACK_FOUR):
                        maxBlack.append(0)
                elif (self.board[i][j] == Cell.WHITE_EMPTY):
                    check = True
                    for k in range (4):
                        nextRow = i + movement[0][k]
                        nextCol = j + movement[1][k]
                        if (nextRow >= 0 and nextCol >= 0 and nextRow < self.rowSize and nextCol < self.colSize):
                            if (self.board[nextRow][nextCol] <= Cell.BLACK_FOUR or self.board[nextRow][nextCol] > Cell.FORBIDDEN):
                                check = False
                    if (check):
                            whitePosition.append([i, j])
        maxBlack = np.array(maxBlack)
        blackPosition = np.array(blackPosition)
        whitePosition = np.array(whitePosition)
        return maxBlack, blackPosition, whitePosition
    
    def preProcZero (self):
        movement = [[0, 1, 0, -1], [1, 0, -1, 0]]
        for i in range (self.rowSize):
            for j in range (self.colSize):
                if (self.board[i][j] == Cell.BLACK_ZERO):
                    for k in range (4):
                         nextRow = i + movement[0][k]
                         nextCol = j + movement[1][k]
                         if (nextRow >= 0 and nextCol >= 0 and nextRow < self.rowSize and nextCol < self.colSize):
                             if (self.board[nextRow][nextCol] == Cell.WHITE_EMPTY):
                                self.board[nextRow][nextCol] = Cell.FORBIDDEN

    def preProc (self):
        movement = [[0, 1, 0, -1], [1, 0, -1, 0]]
        check = False
        for i in range (self.rowSize):
            for j in range (self.colSize):
                if (self.board[i][j] <= Cell.BLACK_FOUR and self.board[i][j] > Cell.BLACK_ZERO):
                    countWhite = 0
                    countLamp = 0
                    whitePosition = []
                    remaining = self.board[i][j]
                    for k in range (4):
                        nextRow = i + movement[0][k]
                        nextCol = j + movement[1][k]
                        if (nextRow >= 0 and nextCol >= 0 and nextRow < self.rowSize and nextCol < self.colSize):
                            if (self.board[nextRow][nextCol] == Cell.WHITE_EMPTY):
                                countWhite += 1
                                whitePosition.append([nextRow, nextCol])
                            elif (self.board[nextRow][nextCol] == Cell.LAMP):
                                countLamp += 1
                                remaining -= 1

                    if (countLamp == self.board[i][j]): self.board[i][j] *= 100
                    elif (countWhite == remaining):
                        check = True
                        for white in whitePosition:
                            self.putSingleLamp(white[0], white[1])
                        self.board[i][j] *= 100
                        print (self.board, '\n')
                elif (self.board[i][j] == Cell.WHITE_EMPTY):
                    checkWhiteCenter = True
                    for k in range (4):
                        nextRow = i + movement[0][k]
                        nextCol = j + movement[1][k]
                        if (nextRow >= 0 and nextCol >= 0 and nextRow < self.rowSize and nextCol < self.colSize):
                            if (self.board[nextRow][nextCol] > Cell.BLACK_ANY):
                                checkWhiteCenter = False
                                break
                    if (checkWhiteCenter): self.putSingleLamp(i, j)
        
        return check
    
    def getWhites (self):
        movement = [[0, 1, 0, -1], [1, 0, -1, 0]]
        whitePosition = []
        for i in range (self.rowSize):
            for j in range (self.colSize):
                if (self.board[i][j] == Cell.WHITE_EMPTY):
                    check = True
                    for k in range (4):
                        nextRow = i + movement[0][k]
                        nextCol = j + movement[1][k]
                        if (nextRow >= 0 and nextCol >= 0 and nextRow < self.rowSize and nextCol < self.colSize):
                            if (self.board[nextRow][nextCol] <= Cell.BLACK_FOUR or self.board[nextRow][nextCol] > Cell.FORBIDDEN):
                                check = False
                    if (check):
                            whitePosition.append([i, j])
        whitePosition = np.array(whitePosition)
        return whitePosition
    
    def setBlackPosition (self, blackPosition):
        self.blackPosition = blackPosition

    def setWhitePosition (self, whitePosition):
        self.whitePosition = whitePosition

    # return board dimension
    # this method is required for Wolf to know on what dimension they used
    def getDimension (self):
        return self.dimension
    
    def fillWhitesOnLastAttempt (self):
        allCheck = False
        for i in range (self.rowSize):
            for j in range (self.colSize):
                if (self.board[i][j] == Cell.WHITE_EMPTY):
                    check = True

                    # check rightside
                    check2 = True
                    for k in range (j+1, self.colSize):
                        if (k >= 0 and k < self.colSize):
                            if (self.board[i][k] == Cell.LAMP or self.board[i][k] == Cell.COLLISION):
                                check = False
                                break
                            elif (self.board[i][k] <= Cell.BLACK_ANY or self.board[i][k] > Cell.FORBIDDEN):
                                break

                    if not check: continue

                    # check leftside
                    for k in range (j-1, -1, -1):
                        if (k >= 0 and k < self.colSize):
                            if (self.board[i][k] == Cell.LAMP or self.board[i][k] == Cell.COLLISION):
                                check = False
                                break
                            elif (self.board[i][k] <= Cell.BLACK_ANY or self.board[i][k] > Cell.FORBIDDEN):
                                break

                    if not check: continue
                    
                    # check downside
                    for k in range (i+1, self.rowSize):
                        if (k >= 0 and k < self.rowSize):
                            if (self.board[k][j] == Cell.LAMP or self.board[k][j] == Cell.COLLISION):
                                check = False
                                break
                            elif (self.board[k][j] <= Cell.BLACK_ANY or self.board[k][j] > Cell.FORBIDDEN):
                                break

                    if not check: continue

                    # check upside
                    for k in range (i-1, -1, -1):
                        if (k >= 0 and k < self.rowSize):
                            if (self.board[k][j] == Cell.LAMP or self.board[k][j] == Cell.COLLISION):
                                check = False
                                break
                            elif (self.board[k][j] <= Cell.BLACK_ANY or self.board[k][j] > Cell.FORBIDDEN):
                                break
                    
                    if not check: continue
                    else: 
                        self.putSingleLamp(i, j)
                        allCheck = True
        return allCheck