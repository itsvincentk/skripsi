# A game played on one board -- with mutiple wolf in that board, all parameters adjusted here.
# A game has: wolf orders

import numpy as np
import random
from Wolf import Wolf
from Board import Board

class Game:
    FIRST_GWO = 0
    SECOND_GWO = 1

    # Experiment type
    EXPERIMENT_SINGLE_WHITE = 'SINGLE_WHITE' # take only alpha board from first GWO, and then the second encoding is all white squares that are not lit on alpha board
    EXPERIMENT_SINGLE_X = 'SINGLE_X' # take only alpha board from first GWO, and then the second encoding is all white squares that are not around black squares 1--4

    def __init__(self, populationCount, seed, punishments, epoch, board) -> None:
        self.populationCount = populationCount
        self.seed = seed
        self.board = Board(board)
        random.seed(seed)
        np.random.seed(seed)
        self.punishments = punishments
        self.epoch = epoch

   
    def startExperiment (self, encodingType, rankNumber, preprocStatus):
        # preproc
        if (preprocStatus):
            #print (self.board.board)
            self.board.preProcZero()
            #print (self.board.board)
            while (self.board.preProc()): continue
        maxBlack, blackPosition, whitePosition = self.board.countEncodingDimension()
        firstAlpha, status = self.firstGWO(maxBlack, blackPosition, self.board.board)
        if (status): firstAlpha = firstAlpha[:rankNumber]
        #print ("AAAAA")
        #print (firstAlpha[0].board.board)
        answer = None
        max = 2**31 - 1
        for wolf in firstAlpha:
            if (encodingType == Game.EXPERIMENT_SINGLE_WHITE):
                whitePosition = wolf.board.getWhites()
            lastAlpha = self.secondGWO(whitePosition, wolf.board.board)
            #print (lastAlpha.fitness)
            #print (lastAlpha.board.board)
            if (lastAlpha.fitness < max):
                answer = lastAlpha
                max = lastAlpha.fitness
            if (max == 0):
                #print (answer.fitness)
                #print (answer.board.board)
                break
        print (answer.board.board)
        return answer

    def firstGWO (self, maxBlack, blackPosition, board):
        #print (blackPosition, "\n")
        if (blackPosition.size == 0):
            return [Wolf(board, self.seed, self.punishments)], False
        population = []
        # create wolf population
        for _ in range (self.populationCount):
            population.append(Wolf(board, self.seed, self.punishments))
        dimension = maxBlack.shape[0]
        for wolf in population:
            wolf.board.setBlackPosition(blackPosition)
            initPosition = []
            for maxNum in maxBlack:
                initPosition.append(random.randint(0,maxNum))
            initPosition = np.array(initPosition)
            wolf.board.copyBoard()
            wolf.updatePosition(initPosition, Board.BLACK_LAMP)
        population.sort(key = lambda wolf : wolf.fitness)
        alpha = population[0]
        beta = population[1]
        delta = population[2]
        a = 2 # var 'a' from GWO algorithm
        for i in range (self.epoch):
            for wolf in population:
                thisPosition = wolf.blackPosition
                A1 = 2 * a * np.random.sample(size=dimension) - a
                A2 = 2 * a * np.random.sample(size=dimension) - a
                A3 = 2 * a * np.random.sample(size=dimension) - a
                C1 = 2 * np.random.sample(size=dimension) 
                C2 = 2 * np.random.sample(size=dimension) 
                C3 = 2 * np.random.sample(size=dimension) 
                X1 = alpha.blackPosition - A1 * abs(C1 * alpha.blackPosition - thisPosition)
                X2 = beta.blackPosition - A2 * abs(C2 * beta.blackPosition - thisPosition)
                X3 = delta.blackPosition - A3 * abs(C3 * delta.blackPosition - thisPosition)
                newPosition = (X1 + X2 + X3) / 3.0
                newPosition = newPosition % maxBlack
                newPosition = np.round(newPosition).astype(int)
                wolf.updatePosition(newPosition, Board.BLACK_LAMP)
            population.sort(key = lambda wolf : wolf.fitness)
            # update the new alpha, beta, and delta
            alpha = population[0]
            beta = population[1]
            delta = population[2]
            # linear decrease of 'a' from 2 to 0
            a -= i/self.epoch
            # print (alpha.fitness)
        #print (alpha.board.board)
        #print (alpha.fitness)
        #print ("A")
        return population, True

    def secondGWO (self, whitePosition, board):
        #print (whitePosition.shape[0], "\n")
        population = []
        # create wolf population
        for _ in range (self.populationCount):
            population.append(Wolf(board, self.seed, self.punishments))
        dimension = whitePosition.shape[0]
        for wolf in population:
            wolf.board.setWhitePosition(whitePosition)
            initPosition = np.random.randint(2, size=dimension)
            wolf.board.copyBoard()
            wolf.updatePosition(initPosition, Board.WHITE_LAMP)
        population.sort(key = lambda wolf : wolf.fitness)
        alpha = population[0]
        beta = population[1]
        delta = population[2]
        a = 2 # var 'a' from GWO algorithm
        for i in range (self.epoch):
            for wolf in population:
                # linear decrease of 'a' from 2 to 0
                a = 2 - (i/self.epoch)*2
                thisPosition = wolf.whitePosition
                #if (thisPosition[-2] == 1): print (thisPosition)
                A1 = 2 * a * np.random.sample(size=dimension) - a
                A2 = 2 * a * np.random.sample(size=dimension) - a
                A3 = 2 * a * np.random.sample(size=dimension) - a
                C1 = 2 * np.random.sample(size=dimension) 
                C2 = 2 * np.random.sample(size=dimension) 
                C3 = 2 * np.random.sample(size=dimension) 
                X1 = alpha.whitePosition - A1 * abs(C1 * alpha.whitePosition - thisPosition)
                X2 = beta.whitePosition - A2 * abs(C2 * beta.whitePosition - thisPosition)
                X3 = delta.whitePosition - A3 * abs(C3 * delta.whitePosition - thisPosition)
                
                newPosition = (X1 + X2 + X3) / 3.0
                # print ("....")
                # print (a)
                # print (A1)
                # print (A2)
                # print (A3)
                # print (C1)
                # print (C2)
                # print (C3)
                # print (X1)
                # print (X2)
                # print (X3)
                # print (newPosition)
                # print ("....")
                
                newPosition = newPosition % 2
                newPosition = np.round(newPosition).astype(int)
                print (newPosition)
                wolf.updatePosition(newPosition, Board.WHITE_LAMP)
            population.sort(key = lambda wolf : wolf.fitness)
            # update the new alpha, beta, and delta
            alpha = population[0]
            beta = population[1]
            delta = population[2]
            if (alpha.fitness < 1):
                break
        #print (alpha.board.board)
        #print (alpha.fitness)
        return alpha