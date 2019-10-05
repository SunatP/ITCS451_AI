"""This module contains agents that play reversi."""

import abc
import random
import asyncio
import traceback

import numpy as np
import gym
import boardgame2 as bg2
import time



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
        try:
            await self.search(board, valid_actions)
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print(e)
        return self.best_move

    @abc.abstractmethod
    async def search(self, board, valid_actions):
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
            This method should set self._move as a way to return.

        """
        raise NotImplementedError('You will have to implement this.')


class RandomAgent(ReversiAgent):
    """An agent that move randomly."""
    
    async def search(self, board, valid_actions):
        """Set the intended move to self._move."""
        # If you want to "simulate a move", you can call the following function:
        # transition(board, self.player, valid_actions[0])
        await asyncio.sleep(2.0)
        randidx = random.randint(0, len(valid_actions) - 1)
        self._move = valid_actions[randidx]


class SunatAgent(ReversiAgent): # Create Sunat Agent use Alpha-Beta Pruning Search

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
    

    async def search(self, board, valid_actions): # Point to async search
        MAX,MIN = 1000,-1000

        await asyncio.sleep(2.0)
        moving = Alpha_moving(board,self.player,valid_actions[0])
        self._move = valid_actions[moving]
        

        def Alpha_moving(state):
            value = Max_value(state,-float('inf'),float('inf'))
            self._move = valid_actions[value]

        def Max_value(self,alpha,beta):
            alpha = -float('inf')
            beta = float('inf')
            if self.isTerminal(self._move):
                return self.getUtility(self._move)
            value = alpha
            best_state = None
            for a in board:
                value = max(value, Min_value(best_state,a),alpha,beta)
                if value >= beta :
                    return value
                    best_state = a
                    alpha = max(alpha,value)
            return value
            # self._move = best_state[value]
    
        def Min_value(self,alpha,beta):
            alpha = -float('inf')
            beta = float('inf')
            if self.isTerminal(self._move):
                return self.getUtility(self._move)
            value = beta
            best_state = None
            for a in board:
                value = max(value, Max_value(best_state,a),alpha,beta)
                if value <= alpha :
                    return value
                    best_state = a
                    beta = min(beta,value)
            # self._move = best_state[value]
            return value
        # infinity = float('inf')
        # best_val = -infinity
        # beta = infinity
    
        # successors = self.getSuccessors(board)
        # best_state = None
        # scores = np.zeros(len(self.move))
        # for state in self.best_move(board):
        #     # value = self.max_value(state, best_val, beta)
        #     value = max(value, self.min_value(state,best_state))
        #     if value > best_val:
        #         best_val = value
        #         best_state = state
        # return self._move == valid_actions[best_state]
        # alpha = -float('inf') # define as min val
        # beta = float('inf') # define as max val
        # max = -float('inf')
        # best_state = None
        # for i in self.move:
        #     value = self.max(i,alpha,beta)
        #     if max < value:
        #         best_val = value
        #         best_state = i
        # self._move = valid_actions[best_state]
        # print("Fuck You")

    # def min_value(self,node,alpha,beta):
    #     infinity = float('inf')
    #     value = infinity
    #     if self.isTerminal(node):
    #         return self.getUtility(node)
    #     successors = self.getSuccessors(node)
    #     for state in successors:
    #         value = min(value, self.max_value(state, alpha, beta))
    #         if value <= alpha:
    #             return value
    #             # self._move = value[min]
    #         beta = min(beta, value)

    #     # self._move = value[min]
    #     # return value
    #     return self._move == value[beta]
    
    # def max_value(self,node,alpha,beta):
    #     infinity = float('inf')
    #     value = -infinity
    #     if self.isTerminal(node):
    #         return self.getUtility(node)
    #     successors = self.getSuccessors(node)
    #     for state in successors:
    #         value = max(value, self.min_value(state, alpha, beta))
    #         if value >= beta:
    #             return value
    #             # self._move = value[max]
    #         alpha = max(alpha, value)
    #     # return value
    #     return self._move == value[alpha]
    #     # self._move = value[max]

        def getSuccessors(self, node):
            assert node is not None
            return node.children

    # return true if the node has NO children (successor states)
    # return false if the node has children (successor states)
        def isTerminal(self, node):
            assert node is not None
            return len(node.children) == 0

        def getUtility(self, node):
            assert node is not None
            return node.value
        # # max()
        # infinity = float('inf')
        # best_val = np.argmin(infinity)
        # beta = np.argmax(infinity)
        # # successor = self.best_move(board)
        # # best_state = None

        # for state in self.best_move:
        #     print(state)
        #     value = self.max(state,best_val,beta)    
        #     if value > best_val:
        #         alpha = value
        #         self._move = valid_actions[state]
        # await asyncio.sleep(1)
        # print(self._move)
        # # best_val = self.max(valid_actions)
        # # self._move = valid_actions[best_state]
        # print("Sunat Finished")
    
        # def max(self,alpha,beta):
        #     infinity = float('inf')
        #     value = min(infinity)
        #     # successor = self.move(random)
        #     for state in self.best_move:
        #         print(state)
        #         value = max(value, self.min(state,alpha,beta))
        #         if value >= beta:
        #             return value
        #         # alpha = max(alpha,value)
        #         alpha = max(alpha,value)
        #     return value
        # print("Max Visited Node : " + self.max(valid_actions))


        # def min(self,alpha,beta):
        #     infinity = float('inf')
        #     value = max(infinity)
        #     # successor = self.move(random)
        #     for state in self.best_move:
        #         value = min(value, self.max(state,alpha,beta))
        #         if value <= alpha:
        #             return value
        #         # beta = min(alpha,value)
        #         beta = min(alpha,value)
        #     return value
        # print("Max Visited Node : " + self.max(valid_actions))