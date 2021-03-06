"""
This module contains agents that play reversi.

Version 3.1
"""

import abc
import random
import asyncio
import traceback
import time
from multiprocessing import Process, Value
import math
import numpy as np
import gym
import sys
import boardgame2 as bg2
import reversi as rs
import copy


_ENV = gym.make('Reversi-v0')
_ENV.reset()


def transition(board, player, action):
    """Return a new board if the action is valid, otherwise None."""
    if _ENV.is_valid((board, player), action):
        new_board, __ = _ENV.get_next_state((board, player), action)
        return new_board
    return None


class ReversiAgent(abc.ABC):
    """Reversi Agent."""

    def __init__(self, color):
        """
        Create an agent.
        
        Parameters
        -------------
        color : int
            BLACK is 1 and WHITE is -1. We can get these constants
            from bg2.BLACK and bg2.WHITE.

        """
        super().__init__()
        self._move = None
        self._color = color
    
    @property
    def player(self):
        """Return the color of this agent."""
        return self._color

    @property
    def pass_move(self):
        """Return move that skips the turn."""
        return np.array([-1, 0])

    @property
    def best_move(self):
        """Return move after the thinking.
        
        Returns
        ------------
        move : np.array
            The array contains an index x, y.

        """
        if self._move is not None:
            return self._move
        else:
            return self.pass_move

    async def move(self, board, valid_actions):
        """Return a move. The returned is also availabel at self._move."""
        self._move = None
        output_move_row = Value('d', -1)
        output_move_column = Value('d', 0)
        try:
            # await self.search(board, valid_actions)    
            p = Process(
                target=self.search, 
                args=(
                    self._color, board, valid_actions, 
                    output_move_row, output_move_column))
            p.start()
            while p.is_alive():
                await asyncio.sleep(0.1)
        except asyncio.CancelledError as e:
            print('The previous player is interrupted by a user or a timer.')
        except Exception as e:
            print(type(e).__name__)
            print('move() Traceback (most recent call last): ')
            traceback.print_tb(e.__traceback__)
        finally:
            p.kill()
            self._move = np.array(
                [output_move_row.value, output_move_column.value],
                dtype=np.int32)
        return self.best_move

    @abc.abstractmethod
    def search(
            self, color, board, valid_actions, 
            output_move_row, output_move_column):
        """
        Set the intended move to self._move.
        
        The intended move is a np.array([r, c]) where r is the row index
        and c is the column index on the board. [r, c] must be one of the
        valid_actions, otherwise the game will skip your turn.

        Parameters
        -------------------
        board : np.array
            An 8x8 array that contains 
        valid_actions : np.array
            An array of shape (n, 2) where n is the number of valid move.

        Returns
        -------------------
        None
            This method should set value for 
            `output_move_row.value` and `output_move_column.value` 
            as a way to return.

        """
        raise NotImplementedError('You will have to implement this.')


class RandomAgent(ReversiAgent):
    """An agent that move randomly."""
    
    def search(
            self, color, board, valid_actions, 
            output_move_row, output_move_column):
        """Set the intended move to the value of output_moves."""
        # If you want to "simulate a move", you can call the following function:
        # transition(board, self.player, valid_actions[0])

        # To prevent your agent to fail silently we should an
        # explicit trackback printout.
        try:
            # while True:
            #     pass
            time.sleep(3)
            randidx = random.randint(0, len(valid_actions) - 1)
            random_action = valid_actions[randidx]
            output_move_row.value = random_action[0]
            output_move_column.value = random_action[1]
        except Exception as e:
            print(type(e).__name__, ':', e)
            print('search() Traceback (most recent call last): ')
            traceback.print_tb(e.__traceback__)
class PoohAgent(ReversiAgent):

    def __index__(self):
        super(minimax, self)
        # self.transpositionTable = set()

    def search(self, color, board, valid_actions, output_move_row, output_move_column):
        if self._color == 1:
            evaluation, bestAction = self.minimax(board, valid_actions, 4, 0, - sys.maxsize - 1, sys.maxsize, True)
        else:
            evaluation, bestAction = self.minimax(board, valid_actions, 2, 0, - sys.maxsize - 1, sys.maxsize, True)
        # self.createState(board, valid_actions, self._color)

        print("Me Selected: " + str(bestAction))
        output_move_row.value = bestAction[0]
        output_move_column.value = bestAction[1]

    def minimax(self, board: np.array, validActions: np.array, depth: int, levelCount: int, alpha: int, beta: int,
                maximizingPlayer: bool):
        if depth == 0:
            return self.evaluateStatistically(board)

        bestAction: np.array = None
        if maximizingPlayer:
            mAlpha: int = alpha
            maxEval: int = - sys.maxsize - 1 # -float("int")
            player: int = self._color

            for action in validActions:
                newState, newValidActions = self.createState(board, action, player)
                evaluation = self.minimax(newState, newValidActions
                                          , depth - 1, levelCount + 1, mAlpha, beta, not maximizingPlayer)

                if maxEval < evaluation:
                    maxEval = evaluation

                    if levelCount == 0:
                        bestAction = action

                mAlpha = max(mAlpha, evaluation)
                if beta <= mAlpha:
                    break
            if levelCount != 0:
                return maxEval
            else:
                return maxEval, bestAction
        else:
            mBeta: int = beta
            minEval: int = sys.maxsize
            player: int = self.getOpponent(self._color)

            for action in validActions:
                newState, newValidActions = self.createState(board, action, player)
                evaluation = self.minimax(newState, newValidActions
                                          , depth - 1, levelCount + 1, alpha, mBeta, not maximizingPlayer)

                if minEval > evaluation:
                    minEval = evaluation

                    if levelCount == 0:
                        bestAction = action

                mBeta = min(mBeta, evaluation)
                if mBeta <= alpha:
                    break
            if levelCount != 0:
                return minEval
            else:
                return minEval, bestAction

    def evaluateStatistically(self, board: np.array) -> int:
        countA: int = 0
        countB: int = 0
        evalBoard = np.array(list(zip(*board.nonzero())))

        # print("Print Board: " + str(evalBoard))
        for row in evalBoard:
            if board[row[0]][row[1]] == self._color:
                countA += 1
            else:
                countB += 1
        return countA - countB

    @staticmethod
    def getOpponent(player: int):
        if player == 1:
            return -1
        else:
            return 1

    def createState(self, board: np.array, action: np.array, player: int) -> (np.array, np.array):
        newState: np.array = transition(board, player, action)

        validMoves: np.array = _ENV.get_valid((newState, self.getOpponent(player)))
        validMoves: np.array = np.array(list(zip(*validMoves.nonzero())))

        return newState, validMoves
        
class AgentMongChaChaVI(ReversiAgent):
    """An agent that evaluates each action using trained weights"""

    def __init__(self, color: int):
        """
        Initialize the weight matrix
        :param color: color of the current agent. It can be only either BLACK or WHITE
        """
        super().__init__(color)
        weights = (80, -26, 24, -1, -5, 28, -18, 76,
                   -23, -39, -18, -9, -6, -8, -39, -1,
                   46, -16, 4, 1, -3, 6, -20, 52,
                   -13, -5, 2, -1, 4, 3, -12, -2,
                   -5, -6, 1, -2, -3, 0, -9, -5,
                   48, -13, 12, 5, 0, 5, -24, 41,
                   -27, -53, -11, -1, -11, -16, -58, -15,
                   87, -25, 27, -1, 5, 36, -3, 100)
        self.trainedWeights = np.array(weights).reshape(8, 8)
        # print(self.trainedWeights)

    def search(self, color, board, valid_actions, output_move_row, output_move_column):
        """
        Begins searching for a round of the game
        :param color:               the color of the current player.
        :param board:               the state of the board
        :param valid_actions:       the executable actions for the current player
        :param output_move_row:     the variable to store the outcome of searching in ROW manner
        :param output_move_column:  the variable to store the outcome of searching in ROW manner
        :return:                    nothing
        """

        # Hard-coded statements for testing against the same type of agent
        if self._color == 1:
            evaluation, bestAction = self.minimax(board, valid_actions, 4, 0, -99999, 99999, True)
        else:
            evaluation, bestAction = self.minimax(board, valid_actions, 4, 0, -99999, 99999, True)

        print("Me Selected: " + str(bestAction))

        # Stupid error messages avoidance
        if bestAction is not None:
            output_move_row.value = bestAction[0]
            output_move_column.value = bestAction[1]

    def minimax(self, board: np.array, validActions: np.array, depth: int, levelCount: int, alpha: int, beta: int,
                maximizingPlayer: bool):
        """
        Recursively find the optimal action based on the current observation.
        The algorithm is Minimax with Alpha-Beta pruning
        :param board:               the state of the board
        :param validActions:        executable actions for the current player
        :param depth:               depth limit for recursive Minimax
        :param levelCount:          depth counter
        :param alpha:               alpha value for pruning the Search tree
        :param beta:                beta value for pruning the Search tree
        :param maximizingPlayer:    determine whether the current Minimax node is a Maximizing node or not
        :return:                    At levelCount == 0: returns eval and bestAction; otherwise, returns only eval.
        """
        if depth == 0:
            return self.evaluateStatistically(board)

        bestAction: np.array = None
        if maximizingPlayer:
            mAlpha: int = alpha
            maxEval: int = -99999
            player: int = self._color

            for action in validActions:
                newState, newValidActions = self.createState(board, action, player)
                evaluation = self.minimax(newState, newValidActions,
                                          depth - 1, levelCount + 1, mAlpha, beta, not maximizingPlayer)

                if maxEval < evaluation:
                    maxEval = evaluation

                    if levelCount == 0:
                        bestAction = action

                mAlpha = max(mAlpha, evaluation)
                if beta <= mAlpha:
                    break
            if levelCount != 0:
                return maxEval
            else:
                return maxEval, bestAction
        else:
            mBeta: int = beta
            minEval: int = 99999
            player: int = self.getOpponent(self._color)

            for action in validActions:
                newState, newValidActions = self.createState(board, action, player)
                evaluation = self.minimax(newState, newValidActions,
                                          depth - 1, levelCount + 1, alpha, mBeta, not maximizingPlayer)

                if minEval > evaluation:
                    minEval = evaluation

                    if levelCount == 0:
                        bestAction = action

                mBeta = min(mBeta, evaluation)
                if mBeta <= alpha:
                    break
            if levelCount != 0:
                return minEval
            else:
                return minEval, bestAction

    def evaluateStatistically(self, board: np.array) -> int:
        """
        Calculates the Evaluation at the depth limit
        :param board:   current state of the board
        :return:        evaluation value
        """

        nonZeroPositions = np.array(list(zip(*board.nonzero())))

        myEvaluationScore = 0
        opponentEvaluationScore = 0

        for position in nonZeroPositions:
            positionY, positionX = position[0], position[1]

            # If the current position has a piece of this Agent
            if board[positionY][positionX] == self._color:
                # Get the weight from hard-coded matrix
                myEvaluationScore += self.trainedWeights[positionY][positionX]
            else:
                opponentEvaluationScore += self.trainedWeights[positionY][positionX]

        # The differences between this Agent and its opponent.
        return myEvaluationScore - opponentEvaluationScore

    @staticmethod
    def getOpponent(player: int):
        """
        Returns the opponent player identifier
        :param player:      a player
        :return:            the opponent of that player
        """
        if player == 1:
            return -1
        else:
            return 1

    def createState(self, board: np.array, action: np.array, player: int) -> (np.array, np.array):
        """
        Creates a new state and new actions based on given a state and an action.
        :param board:       a state of the board
        :param action:      an action
        :param player:      a player that performs the action
        :return:            a new state and a set of new possible actions
        """
        newState: np.array = transition(board, player, action)

        validMoves: np.array = _ENV.get_valid((newState, self.getOpponent(player)))
        validMoves: np.array = np.array(list(zip(*validMoves.nonzero())))

        return newState, validMoves


class StupidCountingAgent(AgentMongChaChaVI):

    def __init__(self, color):
        super().__init__(color)

        # self.transpositionTable = set()

    def evaluateStatistically(self, board: np.array) -> int:
        """
        Stupidly counts all pieces on the board
        :param board:       a state of the board
        :return:            the difference between both players in terms of piece counts
        """
        countA: int = 0
        countB: int = 0

        # Eliminates all ZEROES in the board and return NON-ZERO as a position (Row, Col)
        nonZeroPositions = np.array(list(zip(*board.nonzero())))

        # print("Print Board: " + str(nonZeroPositions))
        for position in nonZeroPositions:
            if board[position[0]][position[1]] == self._color:
                countA += 1
            else:
                countB += 1
        return countA - countB


class KrittametNoobsAgent(ReversiAgent):
    def __index__(self):
        super(KrittametNoobsAgent,self)

    def scoreCompareEvaluator(self,board,action):
        color:int = self._color
        countA: int = 0
        countB: int = 0
        countA_after: int = 0
        countB_after: int = 0
        evalBoard = np.array(list(zip(*board.nonzero())))

        newBoard, newPossibleMove = self.createState(board,action,color)

        for row in evalBoard:
            if board[row[0]][row[1]] == self._color:
                countA += 1
            else:
                countB += 1
        if (countA - countB) < 0:
            return countA - countB

        return countA + (countA - countB) - len(newPossibleMove)    #return current score + improvements

    def maxEatEvaluator(self,board,action):

        color:int = self._color

        #before place
        countBefore = 0
        countAfter = 0
        evalBoard = np.array(list(zip(*board.nonzero())))
        for row in evalBoard:
            if board[row[0]][row[1]] == self._color:
                countBefore += 1

        #after place
        newBoard, newPossibleMove = self.createState(board,action,color)
        for row in evalBoard:
            if newBoard[row[0]][row[1]] == self._color:
                countAfter += 1
        
        return countAfter - countBefore

    def search(self, color, board, valid_actions, output_move_row, output_move_column):
        print("Noob Kok is trying hard")
        try:
            bestMove = self.MAX_NODE(board, valid_actions,0,2,float('-inf'),float('inf'),self.scoreCompareEvaluator)
            if bestMove is None:
                print("Noob Kok is panicing")
                bestMove = self.MAX_NODE(board, valid_actions,0,0,float('-inf'),float('inf'),self.maxEatEvaluator)
                output_move_row.value = bestMove[0]
                output_move_column.value = bestMove[1]
            else:
                output_move_row.value = bestMove[0]
                output_move_column.value = bestMove[1]
                print("Choose:" + str(bestMove))
        except Exception as e:
            print(type(e).name, ':', e)
            print('search() Traceback (most recent call last): ')
            traceback.print_tb(e.traceback)
    
    def MAX_NODE(self, board:np.array, possibleMove: np.array, depth:int, depthLimit:int, alpha:float, beta:float,evaluator):

        if depth == depthLimit:      #in case no future prediction
            #calculate score of this node
            maxscore = 0
            bestchoice:np.array = None
            for action in possibleMove:
                score = evaluator(board,action)
                if score > maxscore:
                    maxscore = score
                    bestchoice = action

            return maxscore

        a = alpha
        b = beta
        best_move:np.array = None
        color:int = self._color

        for action in possibleMove:
            newBoard, newPossibleMove = self.createState(board,action,color)
            evaluated = self.MIN_NODE(newBoard, newPossibleMove, depth+1, depthLimit, a,b,evaluator)
            if evaluated > a:
                a = evaluated
                best_move = action
            if a >= b:
                break

        if depth == 0:
            return best_move
        else:
            return a

    def MIN_NODE(self, board:np.array, possibleMove: np.array, depth:int, depthLimit:int, alpha:float, beta:float, evaluator):
        if depth == depthLimit:
            #calculate score of this node
            minscore = 999999
            bestchoice:np.array = None
            for action in possibleMove:
                score = evaluator(board,action)
                if score < minscore:
                    minscore = score
                    bestchoice = action

            return minscore
        
        a = alpha
        b = beta
        best_move:np.array = None
        color:int = self.getOpponent(self._color)
    
        for action in possibleMove:
            newBoard, newPossibleMove = self.createState(board,action,color)
            evaluated = self.MAX_NODE(newBoard,newPossibleMove, depth+1, depthLimit,a,b,evaluator)

            if evaluated < b:
                b = evaluated
                best_move = action
            if a >= b:
                break

        if depth == 0:
            return best_move
        else:
            return b
                
    @staticmethod
    def getOpponent(player: int):
        if player == 1:
            return -1
        else:
            return 1   

    def createState(self, board: np.array, action: np.array, player: int) -> (np.array, np.array):
        newState: np.array = transition(board, player, action)

        validMoves: np.array = _ENV.get_valid((newState, self.getOpponent(player)))
        validMoves: np.array = np.array(list(zip(*validMoves.nonzero())))

        return newState, validMoves 


class PolAgent(ReversiAgent):
    def search(self, color, board, valid_action, output_move_row, output_move_column):
        try:
            evaluation, best_state = self.Max_value(board,valid_action,4,0,-99999,99999)
            output_move_row.value = best_state[0]
            output_move_column.value = best_state[1]
        except Exception as e:
            print(type(e).__name__, ':', e)
            print('search() Traceback (most recent call last): ')
            traceback.print_tb(e.__traceback__)


    def Max_value(self,board:np.array,validactions:np.array,depth:int,level:int,alpha:int, beta:int):
        if depth == 0:
            return self.Evalustatis(board)
            
        best_state: np.array=None
        Maxalpha: int = alpha
        Maxevaluation = -99999
        player: int = self._color

        for Actions in validactions:
            newboard, newaction = self.createState(board, Actions, player)
            newmove = self.Min_value(newboard, newaction, depth - 1, level + 1, Maxalpha, beta)
            if Maxevaluation < newmove:
                Maxevaluation = newmove
                if level == 0:
                    best_state = Actions

            Maxalpha = max(Maxalpha, Maxevaluation)
            if beta <= Maxalpha:
                break

        if level != 0:
            return Maxevaluation
        else:
            return Maxevaluation, best_state

    def Min_value(self, board: np.array, validactions: np.array, depth: int, level: int, alpha: int, beta: int):
        if depth == 0:
            return self.Evalustatis(board)

        MinBeta: int = beta
        Minevaluation = 99999
        player: int = self.getOpponent(self._color)
        best_state: np.array = None
        for a in validactions:
            newstate, newaction = self.createState(board, a, player)
            newstep = self.Max_value(newstate, newaction, depth - 1, level + 1, alpha, MinBeta)

            if Minevaluation > newstep:
                Minevaluation = newstep
                if level == 0:
                    best_state = a

            MinBeta = min(MinBeta, Minevaluation)
            if MinBeta <= alpha:
                break
        if level != 0:
            return Minevaluation
        else:
            return Minevaluation, best_state


    def Evalustatis(self, board: np.array) -> int:
        MyScore = 0
        OpponentScore = 0
        total = 0
        evalBoard = np.array(list(zip(*board.nonzero())))

        for position in evalBoard:
            Y, X = position[0], position[1]
            if board[Y][X] == self._color:
                MyScore += (board[Y][X])
            else:
                OpponentScore += (board[Y][X])
                # print(" Eval Score: ", total)
            total = MyScore - OpponentScore
        return (MyScore - OpponentScore)

    @staticmethod
    def getOpponent(player: int):
        if player == 1:
            return -1
        else:
            return 1

    def createState(self, board: np.array, action: np.array, player: int) -> (np.array, np.array):
        newState: np.array = transition(board, player, action)

        validMoves: np.array = _ENV.get_valid((newState, self.getOpponent(player)))
        validMoves: np.array = np.array(list(zip(*validMoves.nonzero())))

        return newState, validMoves


class Old_Chocobo(ReversiAgent):  # Create Sunat Agent use Alpha-Beta Pruning Search

    """
    Alpha-Beta Pruning Search Algorithm limit with 10
    -----------------------------------------------
    function ABS(state) return action
    v <- Max_value(state,+inf,-inf) # v = Max_Value
    -----------------------------------------------
    function Max_value(state,alpha,beta) return a utility value
    if Terminal-test(state) then return utility(state)
    v <- (-inf)  # we can define -inf as float('-inf') or -float('inf)
    for each a in action(state) do
    v <- max(v,Min_Value(Result(s,a),alpha,beta))
    if v >= beta then return v
    alpha <- max(alpha,v)
    return v
    -----------------------------------------------
    function Min_value(state,alpha,beta) return a utility value
    if Terminal-test(state) then return utility(state)
    v <- (inf)
    for each a in action(state) do
    v <- min(v,Max_Value(Result(s,a),alpha,beta))
    if v <= alpha then return v
    beta <- max(beta,v)
    return v
    -----------------------------------------------
    function alphabeta(node, depth, α, β, maximizingPlayer) is
    if depth = 0 or node is a terminal node then
        return the heuristic value of node
    if maximizingPlayer then
        value := −∞
        for each child of node do
            value := max(value, alphabeta(child, depth − 1, α, β, FALSE))
            α := max(α, value)
            if α ≥ β then
                break (* β cut-off *)
        return value
    else
        value := +∞
        for each child of node do
            value := min(value, alphabeta(child, depth − 1, α, β, TRUE))
            β := min(β, value)
            if α ≥ β then
                break (* α cut-off *)
        return value
    (* Initial call *)
    alphabeta(origin, depth, −∞, +∞, TRUE)
    """

    def __init__(self, color):
        super().__init__(color)
        # Create Weight table for Othello that we know is 8x8
        SQUARE_WEIGHTS = [
            0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
            0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
            0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
            0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
            0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
            0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
            0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
            0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
            0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
            0,   0,   0,   0,   0,   0,   0,   0,   0,   0, ]

        self.weight_condition = np.array(
            SQUARE_WEIGHTS, dtype=np.int32).reshape(10, 10)

        # Max_value = sum(map(abs,SQUARE_WEIGHTS))
        # Min_value = -Max_value
        # print(self.weight_condition.reshape) print for get the shape of Weight table
        # print(self.weight_condition.ndim) print for get the shape dimension

    def __index__(self):
        super(Old_Chocobo, self)

    # Instead Alpha Beta Search
    def search(self, color, board, valid_actions, output_move_row, output_move_column):
        # time.sleep(0.03125)
        # print(" Chocobo AI is Thinking...")
        try:
            if self._color == 1:
                evaluation, best_state = self.Max_value(
                    board, valid_actions, 4, 0, -99999, 99999, True)
            else:
                evaluation, best_state = self.Max_value(
                    board, valid_actions, 4, 0, -99999, 99999, True)
            # print("  ", evaluation, best_state)
            if best_state is None or valid_actions is None:
                # time.sleep(0.01625)
                # randidx = random.randint(0, len(valid_actions) - 1)
                # implement with random by using board control
                randidx = random.randint(0, len(self.weight_condition)-10)
                random_action = valid_actions[randidx]
                output_move_row.value, output_move_column.value = random_action[0], random_action[1]
                print(" Chocobo Random Selected:" + str(random_action))
                # time.sleep(0.0625)
            elif best_state is not None:
                # time.sleep(0.03125)
                # We can decided to decrease sleep time or remove it with print output
                # print(" Chocobo is making the decision")
                # time.sleep(0.03125)
                output_move_row.value, output_move_column.value = best_state[0], best_state[1]
                print(" Chocobo Selected:" + str(best_state) +
                      " Evaluated Score: " + str(evaluation))
                # time.sleep(0.03125)
                # we found depth level between 1 - 4 is found solution quicker
                # Sunat_Action = valid_actions[moving]
                # print(" Sunat Selected:" + str(best_state))
        except Exception as e:
            print(type(e).__name__, ':', e)
            print('search() Traceback (most recent call last): ')
            traceback.print_tb(e.__traceback__)

    def Max_value(self, board: np.array, validactions: np.array, depth: int, level: int, alpha: int, beta: int, gain: bool):
        if depth == 0:
            return self.evaluateStatistically(board)

        best_state: np.array = None
        MaxAlpha: int = alpha
        Maxevaluation = -99999
        player: int = self._color

        for a in validactions:
            newstate, newaction = self.createState(board, a, player)
            newstep = self.Min_value(
                newstate, newaction, depth-1, level + 1, MaxAlpha, beta, not gain)
            if Maxevaluation < newstep:
                Maxevaluation = newstep
                if level == 0:
                    best_state = a

            MaxAlpha = max(MaxAlpha, Maxevaluation)
            if beta <= MaxAlpha:
                break

        if level != 0:
            return Maxevaluation
        else:
            self._move = best_state
            # print(self._move)
            return self.evaluateStatistically(board), best_state

    def Min_value(self, board: np.array, validactions: np.array, depth: int, level: int, alpha: int, beta: int, gain: bool):
        if depth == 0:
            return self.evaluateStatistically(board)

        MinBeta: int = beta
        Minevaluation = 99999
        player: int = self.getOpponent(self._color)
        best_state: np.array = None
        for a in validactions:
            newstate, newaction = self.createState(board, a, player)
            newstep = self.Max_value(
                newstate, newaction, depth-1, level + 1, alpha, MinBeta, not gain)

            if Minevaluation > newstep:
                Minevaluation = newstep
                # print(depth)
                if level == 0:
                    best_state = a

            MinBeta = min(MinBeta, Minevaluation)
            if MinBeta <= alpha:
                break
        if level != 0:
            return Minevaluation
        else:
            self._move = best_state
            # print(self._move)
            return self.evaluateStatistically(board), best_state

    def evaluateStatistically(self, board: np.array) -> int:
        MyScore = 0
        OpponentScore = 0
        total = 0
        new_weight = copy.deepcopy(self.weight_condition)
        evalBoard = np.array(list(zip(*board.nonzero()))).T
        # np.array([output_move_row.value, output_move_column.value], dtype=np.int32)
        # print("Print Board: " + str(evalBoard))
        for position in evalBoard:
            Y, X = position[0], position[1]
            if board[Y][X] == self._color:
                MyScore += (new_weight[Y][X] + board[Y][X])
            else:
                OpponentScore += (new_weight[Y][X] + board[Y][X])
        # print(" Eval Score: ", total)
            # total = MyScore - OpponentScore
        return (MyScore - OpponentScore)

    @staticmethod
    def getOpponent(player: int):
        if player == 1:
            return -1
        else:
            return 1

    def createState(self, board: np.array, action: np.array, player: int) -> (np.array, np.array):
        newState: np.array = transition(board, player, action)

        validMoves: np.array = _ENV.get_valid(
            (newState, self.getOpponent(player)))
        validMoves: np.array = np.array(
            list(zip(*validMoves.nonzero())), dtype=np.int32)

        return newState, validMoves
