"""A module for homework 2. Version 3."""
# noqa: D413

import abc
import trace
import copy
import heapq
import itertools
from collections import defaultdict
from typing import List, Any

from hw1 import EightPuzzleState, EightPuzzleNode


def eightPuzzleH1(state, goal_state):
    """
    Return the number of misplaced tiles including blank.

    Parameters
    ----------
    state : EightPuzzleState
        an 8-puzzle state containing a board (List[List[int]])
    goal_state : EightPuzzleState
        a desired 8-puzzle state.

    Returns
    ----------
    int

    """
    # TODO 1:
    sum = 0
    
    for x,y in range(3,3): # range 3 for x and 3 for y
        if (goal_state.board[x][y] != state.board[x][y]):
            sum += 1
    return sum
    pass


def eightPuzzleH2(state, goal_state):
    """
    Return the total Manhattan distance from goal position of all tiles.

    Parameters
    ----------
    state : EightPuzzleState
        an 8-puzzle state containing a board (List[List[int]])
    goal_state : EightPuzzleState
        a desired 8-puzzle state.

    Returns 
    ----------
    int

    """
    # TODO 2:
   
    Manhattansum = 0
    for num in range(9):
        for i in range(len(goal_state.board)):
            for j in range(len(goal_state.board)):
                if goal_state.board[i][j] == num:
                    goal_position = (i, j)
                if goal_state.board[i][j] == num:
                    cur_positions = (i, j)

        Manhattansum += abs(goal_position[0] - cur_positions[0]) + abs(goal_position[1] - cur_positions[1])

    return Manhattansum
    


class Frontier(abc.ABC):
    """An abstract class of a frontier."""

    def __init__(self):
        """Create a frontier."""
        raise NotImplementedError()

    @abc.abstractmethod
    def is_empty(self):
        """Return True if empty."""
        raise NotImplementedError()
    
    @abc.abstractmethod
    def add(self, node):
        """
        Add a node into the frontier.

        Parameters
        ----------
        node : EightPuzzleNode

        Returns  
        ----------
        None

        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def next(self):
        """
        Return a node from a frontier and remove it.

        Returns
        ----------
        EightPuzzleNode

        Raises
        ----------
        IndexError
            if the frontier is empty.

        """
        raise NotImplementedError()


class DFSFrontier(Frontier):
    """An example of how to implement a depth-first frontier (stack)."""

    def __init__(self):
        """Create a frontier."""
        self.stack = []

    def is_empty(self):
        """Return True if empty."""
        return len(self.stack) == 0

    def add(self, node):
        """
        Add a node into the frontier.
        
        Parameters
        ----------
        node : EightPuzzleNode

        Returns
        ----------
        None

        """
        for n in self.stack:
            # HERE we assume that state implements __eq__() function.
            # This could be improve further by using a set() datastructure,
            # by implementing __hash__() function.
            if n.state == node.state:
                return None
        self.stack.append(node)

    def next(self):
        """
        Return a node from a frontier and remove it.

        Returns
        ----------
        EightPuzzleNode

        Raises
        ----------
        IndexError
            if the frontier is empty.

        """
        return self.stack.pop()


class GreedyFrontier(Frontier):
    """A frontier for greedy search."""

    def __init__(self, h_func, goal_state):
        """
        Create a frontier.

        Parameters
        ----------
        h_func : callable h(state, goal_state)
            a heuristic function to score a state.
        goal_state : EightPuzzleState
            a goal state used to compute h()

        """
        self.h = h_func
        self.goal = goal_state
        self.queue = [] # create an empty List array 
        self.enqueued = {} # create an empty Dict array
        self.counter = itertools.count() # an iterator of evenly spaced values, starting at n, and progressing by step. 
        
    pass

    def is_empty(self):
        return len(self.queue) == 0

    def add(self,node: EightPuzzleNode):
        if node in self.enqueued: 
            node = self.enqueued.pop(node) # remove and return last value from index value
            node[-1] = REMOVED # defined as Negative list (refer Last element in array)
        count = next(self.counter)
        
        priority = self.h(node.state, self.goal) 
        entry = [priority, count, node] 
        self.enqueued[node] = entry
        heapq.heappush(self.queue,entry)
        pass

    def next(self):
        while self.queue:
            priority, count, node = heapq.heappop(self.queue)
            if node is not REMOVED: 
                del self.enqueued[node]
                return node


        # TODO: 3
        # Note that you have to create a data structure here and
        # implement the rest of the abstract methods.

REMOVED = -9999 # defined value out of range
    
class AStarFrontier(Frontier):
    """A frontier for greedy search."""

    def __init__(self, h_func, goal_state):
        """
        Create a frontier.

        Parameters
        ----------
        h_func : callable h(state)
            a heuristic function to score a state.
        goal_state : EightPuzzleState
            a goal state used to compute h()


        """
        self.h = h_func
        self.goal = goal_state
        self.queue = [] # create an empty List array 
        self.enqueued = {} # create an empty Dict array
        self.counter = itertools.count() # an iterator of evenly spaced values, starting at n, and progressing by step. 
        # TODO: 4
        # Note that you have to create a data structure here and
        # implement the rest of the abstract methods.

    def is_empty(self):
        return len(self.queue) == 0 # return empty array

    def add(self, node: EightPuzzleNode):
        if node in self.enqueued:
            node = self.find.pop(node) # remove and return last value from index value
            node[-1] = REMOVED # defined as Negative list (refer Last element in array)
        count = next(self.counter)
        priority = node.path_cost + self.h(node.state, self.goal) # calculate node path cost and heuristic function.
        entry = [priority, count, node] # create list array 
        self.enqueued[node] = entry
        heapq.heappush(self.queue, entry)


    def next(self):
        while self.queue:
            priority, count, node = heapq.heappop(self.queue)
            if node is not REMOVED:
                del self.enqueued[node]
                return node

def _parity(board):
    """Return parity of a square matrix."""
    inversions = 0
    nums = []
    for row in board:
        for value in row:
            nums.append(value)
    for i in range(len(nums)):
        for j in range(i+ 1, len(nums)):
            if nums[i] != 0 and nums[j] != 0 and nums[i] > nums[j]:
                inversions += 1
    return inversions % 2


def _is_reachable(board1, board2):
    """Return True if two N-Puzzle state are reachable to each other."""
    return _parity(board1) == _parity(board2)


def graph_search(init_state, goal_state, frontier):
    """
    Search for a plan to solve problem.

    Parameters
    ----------
    init_state : EightPuzzleState
        an initial state
    goal_state : EightPuzzleState
        a goal state
    frontier : Frontier
        an implementation of a frontier which dictates the order of exploreation.
    
    Returns
    ----------
    plan : List[string] or None
        A list of actions to reach the goal, None if the search fails.
        Your plan should NOT include 'INIT'.
    num_nodes: int
        A number of nodes generated in the search.

    """
    if not _is_reachable(init_state.board, goal_state.board):
        return None, 0
    if init_state.is_goal(goal_state.board):
        return [], 0
    num_nodes = 0
    solution = []
    # Perform graph search
    root_node: EightPuzzleNode = EightPuzzleNode(init_state, action='INIT')
    frontier.add(root_node)
    num_nodes += 1

   
    # TODO: 5
    set_node = set()

    while frontier.is_empty() == False:
        current = frontier.next()
        if current.state.is_goal() == True:
            result = current
            break

        if current.state not in set_node:
            set_node.add(current.state)

            num_nodes += 1
            Nodes=[]
            board = copy.deepcopy(init_state.action_space)
            if current.state.y - 1 < 0:
                board.remove('u')
            if current.state.y + 1 > len(init_state.board) - 1:
                board.remove('d')
            if current.state.x - 1 < 0:
                board.remove('l')
            if current.state.x + 1 > len(init_state.board[0]) - 1:
                board.remove('r')
            for i in board:
                EightPuzzleState2 = current.state.successor(i)
                Nodes.append(EightPuzzleNode(EightPuzzleState2, current, i))
            for i in Nodes:
                frontier.add(i)
    path = result.trace()
    path.pop(0) # Remove -INIT
    for i in path:
        solution.append(i.action)
    return solution, num_nodes


def test_by_hand(verbose=True):
    """Run a graph-search."""
    goal_state = EightPuzzleState([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    init_state = EightPuzzleState.initializeState()
    while not _is_reachable(goal_state.board, init_state.board):
        init_state = EightPuzzleState.initializeState()
    # frontier = GreedyFrontier(eightPuzzleH2,goal_state)
    frontier = AStarFrontier(eightPuzzleH1,goal_state)
    #frontier = DFSFrontier()  # Change this to your own implementation.
    if verbose: 
        print(init_state)
    plan, num_nodes = graph_search(init_state, goal_state, frontier)
    if verbose: 
        print(f'A solution is found after generating {num_nodes} nodes.')                        
    if verbose: 
        for action in plan:
            print(f'- {action}')
    return len(plan), num_nodes


def experiment(n=10000):
    """Run experiments and report number of nodes generated."""
    result = defaultdict(list)
    for __ in range(n):
        d, n = test_by_hand(False)
        result[d].append(n)
    max_d = max(result.keys())
    for i in range(max_d + 1):
        n = result[d]
        if len(n) == 0:
            continue    
        print(f'{d}, {len(n)}, {sum(n)/len(n)}')

if __name__ == '__main__':
    __, __ = test_by_hand()
    # experiment()  #  run graph search 10000 times and report result.
