"""A module for homework 2. Version 3."""
# noqa: D413

import abc
import copy
import itertools
from collections import defaultdict
import heapq
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
    #print(state.board)
    #print(goal_state.board)
    count = 0
    for i in range(3):
        for j in range(3):
            if state.board[i][j] != goal_state.board[i][j]:
                count += 1
                #print(count)
    # TODO 1:
    return count


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
    int"""
                            
    import math
    b = state.board
    g = goal_state.board
   # print(state.board)
    manh_dist = 0
    for i in range (3):
        for j in range (3):
            node = state.board[i][j]
            row_b = i
            column_b = j
            for x in range(3):
                for y in range(3):
                    if state.board[i][j] == goal_state.board[x][y]:
                        row_g = x
                        column_g = y
                        x=0
                        y=0            
            manh_dist += (math.fabs(row_g - row_b) + math.fabs(column_g - column_b))
    return manh_dist   
    # TODO 2:


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
        self.stack = []
        self.find = {}
        self.counter = itertools.count()
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
        if node in self.find:
          self.remove(node)
        count = next( self.counter )
        prior = self.h(node.state,self.goal)
        entry = [prior, count, node]
        self.find[node] = entry
        heapq.heappush(self.stack,entry)
        """for n in self.stack:
            # HERE we assume that state implements __eq__() function.
            # This could be improve further by using a set() datastructure,
            # by implementing __hash__() function.
            if n.state == node.state:
                return None
        self.stack.append(node)"""
        pass

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
        while self.stack:
            prior, count, task = heapq.heappop(self.stack)
            if task is not "REMOVED":
                del self.find[task]
                return task
            raise IndexError("Frontier Empty")
    def remove_task(self,node: EightPuzzleNode):
        entry = self.find.pop(node)
        entry[-1] = "REMOVED"
        pass

    
        # TODO: 3
        # Note that you have to create a data structure here and
        # implement the rest of the abstract methods.

    
class AStarFrontier(Frontier):
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
        self.stack = []
        self.find = {}
        self.counter = itertools.count()
    def is_empty(self):
        """Return True if empty."""
        return len(self.stack) == 0

    def add(self, node: EightPuzzleNode):
        """
        Add a node into the frontier.
        
        Parameters
        ----------
        node : EightPuzzleNode

        Returns
        ----------
        None

        """
        if node in self.find:
          self.remove(node)
        count = next( self.counter )
        prior = self.h(node.state,self.goal)
        entry = [prior, count, node]
        self.find[node] = entry
        heapq.heappush(self.entry)
        for n in self.stack:
            # HERE we assume that state implements __eq__() function.
            # This could be improve further by using a set() datastructure,
            # by implementing __hash__() function.
            if n.state == node.state:
                return None
        self.stack.append(node)
        pass

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
        while self.stack:
            prior, count, task = heapq.heappop(self.stack)
            if task is not REMOVED:
                del self.find[task]
                return task
            raise IndexError("Frontier Empty")
    def remove_task(self,node: EightPuzzleNode):
        entry = self.find.pop(node)
        entry[-1] = REMOVED
    pass
        # TODO: 4
        # Note that you have to create a data structure here and
        # implement the rest of the abstract methods.
REMOVED = -999

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
    root_node = EightPuzzleNode(init_state, action='INIT')
    frontier.add(root_node)
    num_nodes += 1
    setnode = set()
    while frontier.is_empty() == False:
        current = frontier.next()
        if current.state.is_goal() == True:
            result = current
            break

        if current.state not in setnode:
            setnode.add(current.state)

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
    # TODO: 5
    path = result.trace()
    path.pop(0)
    print ( path)
    for i in path:
        solution.append(i.action)
    return solution, num_nodes


def test_by_hand(verbose=True):
    """Run a graph-search."""
    goal_state = EightPuzzleState([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    init_state = EightPuzzleState.initializeState()
    while not _is_reachable(goal_state.board, init_state.board):
        init_state = EightPuzzleState.initializeState()
    frontier = GreedyFrontier(eightPuzzleH1,goal_state)  # Change this to your own implementation.
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
