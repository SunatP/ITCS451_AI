"""
Chocobo 天ぷら (Tempura) Division

with Member
1. POONKASEM KASEMSRI NA AYUTTHAYA	6088071
2. SUNAT PRAPHANWONG 	6088130
3. BARAMEERAK KOONMONGKON	6088156

Code by using VSCode with MagicPython and Python 3.7.3 64 Bit ('Base':conda)
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
                self._move = np.array(
                    [output_move_row.value, output_move_column.value], dtype=np.int32)
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


"""
Init Zone of Chocobo 天ぷら (Tempura)
"""


class Chocobo(ReversiAgent):  # Create Sunat Agent use Alpha-Beta Pruning Search

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
            120, -20,  20,   5,   5,  20, -20, 120,
            -20, -40,  -5,  -5,  -5,  -5, -40, -20,
            20,  -5,  15,   3,   3,  15,  -5,  20,
            5,  -5,   3,   3,   3,   3,  -5,   5,
            5,  -5,   3,   3,   3,   3,  -5,   5,
            20,  -5,  15,   3,   3,  15,  -5,  20,
            -20, -40,  -5,  -5,  -5,  -5, -40, -20,
            120, -20,  20,   5,   5,  20, -20, 120, ]

        self.weight_condition = np.array(
            SQUARE_WEIGHTS, dtype=np.int32).reshape(8, 8)

        # Max_value = sum(map(abs,SQUARE_WEIGHTS))
        # Min_value = -Max_value
        # print(self.weight_condition.reshape) print for get the shape of Weight table
        # print(self.weight_condition.ndim) print for get the shape dimension

    def __index__(self):
        super(Chocobo, self)

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
                randidx = random.randint(0, len(self.weight_condition)-8)
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
        evalBoard = np.array(list(zip(*board.nonzero())))
        # np.array([output_move_row.value, output_move_column.value], dtype=np.int32)
        # print("Print Board: " + str(evalBoard))
        for position in evalBoard:
            Y, X = position[0], position[1]
            if board[Y][X] == self._color:
                MyScore += (new_weight[Y][X])
            else:
                OpponentScore += (new_weight[Y][X])
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


"""
End Zone of Chocobo 天ぷら (Tempura) Division

with Member
1. POONKASEM KASEMSRI NA AYUTTHAYA	6088071
2. SUNAT PRAPHANWONG 	6088130
3. BARAMEERAK KOONMONGKON	6088156

Code by using VSCode with MagicPython and Python 3.7.3 64 Bit ('Base':conda)
This module contains agents that play reversi.

Version 3.1
"""
